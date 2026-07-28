import mimetypes
import os
import re
from pathlib import Path

import requests


IMAGE_DIR = Path("docs/assets/images")

ATTACHMENT_URL_PATTERN = re.compile(
    r"https://github\.com/user-attachments/assets/[a-f0-9-]+",
    re.IGNORECASE,
)

HTML_IMAGE_PATTERN = re.compile(
    r'<img(?P<before>[^>]*?)'
    r'src=["\'](?P<url>'
    r'https://github\.com/user-attachments/assets/[a-f0-9-]+'
    r')["\']'
    r'(?P<after>[^>]*)/?>',
    re.IGNORECASE,
)


def get_html_attribute(tag, attribute):
    match = re.search(
        rf'\b{attribute}=["\']([^"\']*)["\']',
        tag,
        re.IGNORECASE,
    )
    return match.group(1) if match else None


def find_existing_image(image_id):
    matches = list(IMAGE_DIR.glob(f"{image_id}.*"))
    return matches[0] if matches else None


def download_attachment(url):
    image_id = url.rstrip("/").split("/")[-1]

    existing_image = find_existing_image(image_id)
    if existing_image:
        return existing_image

    headers = {
        "User-Agent": "mkdocs-attachment-processor",
        "Accept": "application/octet-stream",
    }

    token = os.environ.get("ATTACHMENT_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=True,
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"::warning::Could not download {url}: {error}")
        return None

    content_type = (
        response.headers
        .get("Content-Type", "")
        .split(";")[0]
        .strip()
        .lower()
    )

    if not content_type.startswith("image/"):
        print(
            f"::warning::The attachment did not return an image: "
            f"{url} ({content_type})"
        )
        return None

    suffix = mimetypes.guess_extension(content_type) or ".png"

    if suffix == ".jpe":
        suffix = ".jpg"

    image_path = IMAGE_DIR / f"{image_id}{suffix}"
    image_path.write_bytes(response.content)

    print(f"Downloaded: {image_path}")

    return image_path


def process_markdown_file(md_file):
    original_content = md_file.read_text(encoding="utf-8")
    urls = set(ATTACHMENT_URL_PATTERN.findall(original_content))

    if not urls:
        return False, []

    replacements = {}
    failed_urls = []

    for url in urls:
        print(f"Found attachment: {url}")

        image_path = download_attachment(url)

        if image_path is None:
            failed_urls.append(url)
            continue

        relative_path = os.path.relpath(
            image_path,
            start=md_file.parent,
        ).replace("\\", "/")

        replacements[url] = relative_path

    def replace_html_image(match):
        original_tag = match.group(0)
        url = match.group("url")

        if url not in replacements:
            return original_tag

        alt_text = get_html_attribute(original_tag, "alt")
        alt_text = alt_text or "Screenshot"

        width = get_html_attribute(original_tag, "width")
        height = get_html_attribute(original_tag, "height")

        attributes = []

        if width:
            attributes.append(f'width="{width}"')

        if height:
            attributes.append(f'height="{height}"')

        attribute_text = ""

        if attributes:
            attribute_text = "{ " + " ".join(attributes) + " }"

        return (
            f"![{alt_text}]"
            f"({replacements[url]})"
            f"{attribute_text}"
        )

    updated_content = HTML_IMAGE_PATTERN.sub(
        replace_html_image,
        original_content,
    )

    # Handles images GitHub inserts using Markdown rather than HTML.
    for url, relative_path in replacements.items():
        updated_content = updated_content.replace(
            url,
            relative_path,
        )

    changed = updated_content != original_content

    if changed:
        md_file.write_text(updated_content, encoding="utf-8")
        print(f"Updated: {md_file}")

    return changed, failed_urls


def main():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    changed = False
    all_failed_urls = []

    for md_file in Path("docs").rglob("*.md"):
        file_changed, failed_urls = process_markdown_file(md_file)

        changed = changed or file_changed
        all_failed_urls.extend(failed_urls)

    if changed:
        print("Attachment processing complete.")
    else:
        print("No attachments were converted.")

    if all_failed_urls:
        print("")
        print("The following attachments could not be downloaded:")

        for url in all_failed_urls:
            print(f"::warning::Could not download attachment: {url}")


if __name__ == "__main__":
    main()