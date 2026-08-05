import html
import mimetypes
import os
import re
from pathlib import Path
from urllib.parse import urlparse

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


def get_html_attribute(tag: str, attribute: str) -> str | None:
    """Read an attribute from an HTML image tag."""

    match = re.search(
        rf'\b{attribute}=["\']([^"\']*)["\']',
        tag,
        re.IGNORECASE,
    )

    return match.group(1) if match else None


def find_existing_image(image_id: str) -> Path | None:
    """Find an attachment that has already been downloaded."""

    matches = list(IMAGE_DIR.glob(f"{image_id}.*"))

    return matches[0] if matches else None


def get_signed_attachment_url(
    attachment_url: str,
    token: str,
    repository: str,
) -> str | None:
    """
    Ask GitHub to render the attachment in the context of the
    private repository.

    GitHub's rendered HTML contains a short-lived signed image URL.
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "text/html",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "mkdocs-attachment-processor",
    }

    payload = {
        "text": (
            f'<img alt="attachment" '
            f'src="{attachment_url}" />'
        ),
        "mode": "gfm",
        "context": repository,
    }

    try:
        response = requests.post(
            "https://api.github.com/markdown",
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(
            "::warning::GitHub could not render attachment "
            f"{attachment_url}: {error}"
        )
        return None

    source_match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        response.text,
        re.IGNORECASE,
    )

    if not source_match:
        print(
            "::warning::GitHub rendered the attachment but "
            "did not return an image URL."
        )
        return None

    signed_url = html.unescape(source_match.group(1))

    if signed_url == attachment_url:
        print(
            "::warning::GitHub did not convert the private "
            "attachment into a signed URL."
        )
        return None

    hostname = urlparse(signed_url).hostname or ""

    allowed_hosts = {
        "private-user-images.githubusercontent.com",
        "user-images.githubusercontent.com",
    }

    if hostname not in allowed_hosts:
        print(
            "::warning::GitHub returned an unexpected image host: "
            f"{hostname}"
        )
        return None

    return signed_url


def download_attachment(
    attachment_url: str,
    token: str,
    repository: str,
) -> Path | None:
    """Download a private GitHub attachment into the repository."""

    image_id = attachment_url.rstrip("/").split("/")[-1]

    existing_image = find_existing_image(image_id)

    if existing_image:
        print(f"Already stored: {existing_image}")
        return existing_image

    signed_url = get_signed_attachment_url(
        attachment_url=attachment_url,
        token=token,
        repository=repository,
    )

    if not signed_url:
        return None

    try:
        # Do not send the GitHub PAT to the signed image host.
        response = requests.get(
            signed_url,
            allow_redirects=True,
            timeout=30,
            headers={
                "User-Agent": "mkdocs-attachment-processor",
            },
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(
            "::warning::Could not download signed attachment "
            f"{attachment_url}: {error}"
        )
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
            "::warning::The signed attachment did not return "
            f"an image: {attachment_url} ({content_type})"
        )
        return None

    suffix = mimetypes.guess_extension(content_type) or ".png"

    if suffix == ".jpe":
        suffix = ".jpg"

    image_path = IMAGE_DIR / f"{image_id}{suffix}"
    image_path.write_bytes(response.content)

    print(f"Downloaded: {image_path}")

    return image_path


def process_markdown_file(
    md_file: Path,
    token: str,
    repository: str,
) -> tuple[bool, list[str]]:
    """Download and replace attachments in one Markdown file."""

    original_content = md_file.read_text(encoding="utf-8")

    urls = set(
        ATTACHMENT_URL_PATTERN.findall(original_content)
    )

    if not urls:
        return False, []

    replacements: dict[str, str] = {}
    failed_urls: list[str] = []

    for url in urls:
        print(f"Found attachment: {url}")

        image_path = download_attachment(
            attachment_url=url,
            token=token,
            repository=repository,
        )

        if image_path is None:
            failed_urls.append(url)
            continue

        relative_path = os.path.relpath(
            image_path,
            start=md_file.parent,
        ).replace("\\", "/")

        replacements[url] = relative_path

    def replace_html_image(match: re.Match) -> str:
        original_tag = match.group(0)
        url = match.group("url")

        if url not in replacements:
            return original_tag

        alt_text = (
            get_html_attribute(original_tag, "alt")
            or "Screenshot"
        )

        width = get_html_attribute(original_tag, "width")
        height = get_html_attribute(original_tag, "height")

        attributes = []

        if width:
            attributes.append(f'width="{width}"')

        if height:
            attributes.append(f'height="{height}"')

        attribute_text = ""

        if attributes:
            attribute_text = (
                "{ " + " ".join(attributes) + " }"
            )

        return (
            f"![{alt_text}]"
            f"({replacements[url]})"
            f"{attribute_text}"
        )

    updated_content = HTML_IMAGE_PATTERN.sub(
        replace_html_image,
        original_content,
    )

    # Also handles attachment URLs inserted using Markdown syntax.
    for url, relative_path in replacements.items():
        updated_content = updated_content.replace(
            url,
            relative_path,
        )

    changed = updated_content != original_content

    if changed:
        md_file.write_text(
            updated_content,
            encoding="utf-8",
        )

        print(f"Updated: {md_file}")

    return changed, failed_urls


def main() -> None:
    token = os.environ.get("ATTACHMENT_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")

    if not token:
        raise SystemExit(
            "ATTACHMENT_TOKEN has not been configured."
        )

    if not repository:
        raise SystemExit(
            "GITHUB_REPOSITORY has not been provided."
        )

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    changed = False
    all_failed_urls: list[str] = []

    for md_file in Path("docs").rglob("*.md"):
        file_changed, failed_urls = process_markdown_file(
            md_file=md_file,
            token=token,
            repository=repository,
        )

        changed = changed or file_changed
        all_failed_urls.extend(failed_urls)

    if changed:
        print("Attachment processing complete.")
    else:
        print("No attachments were converted.")

    if all_failed_urls:
        print("")
        print("Attachments that could not be converted:")

        for url in all_failed_urls:
            print(
                "::warning::Could not convert attachment: "
                f"{url}"
            )


if __name__ == "__main__":
    main()