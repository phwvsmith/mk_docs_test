import os
import re
import requests
from pathlib import Path

IMAGE_DIR = Path("docs/assets/images")

ATTACHMENT_PATTERN = re.compile(
    r"https://github\.com/user-attachments/assets/([a-f0-9\-]+)"
)

IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def process_markdown_file(md_file):
    content = md_file.read_text(encoding="utf-8")

    matches = ATTACHMENT_PATTERN.findall(content)

    if not matches:
        return False

    updated_content = content

    for image_id in matches:
        url = f"https://github.com/user-attachments/assets/{image_id}"

        print(f"Found attachment: {url}")

        image_path = IMAGE_DIR / f"{image_id}.png"

        if not image_path.exists():
            response = requests.get(url, allow_redirects=True, timeout=30)
            response.raise_for_status()

            with open(image_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded: {image_path}")

        relative_path = os.path.relpath(
            image_path,
            start=md_file.parent
        ).replace("\\", "/")

        updated_content = updated_content.replace(
            url,
            relative_path
        )

    md_file.write_text(updated_content, encoding="utf-8")

    return True


def main():
    changed = False

    for md_file in Path("docs").rglob("*.md"):
        if process_markdown_file(md_file):
            changed = True
            print(f"Updated: {md_file}")

    if changed:
        print("Attachment processing complete.")
    else:
        print("No GitHub attachments found.")


if __name__ == "__main__":
    main()
