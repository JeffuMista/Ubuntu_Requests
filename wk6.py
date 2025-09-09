import os
import requests
from urllib.parse import urlparse
import uuid
import hashlib

print("Welcome to the Ubuntu url Image Fetcher")
print("A tool that checks and downloads images from the web")


# Directory to save images
FOLDER = "Fetched_Images"
os.makedirs(FOLDER, exist_ok=True)

# Set maximum allowed file size (e.g., 10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  

# Store hashes to detect duplicates
downloaded_hashes = set()


def get_file_hash(data: bytes) -> str:
    """Compute SHA256 hash of file content."""
    return hashlib.sha256(data).hexdigest()


def fetch_image(url: str):
    """Download and save image from a given URL with safety checks."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Catch HTTP errors

        # Check Content-Type header
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"⚠️ Skipping {url} (not an image, Content-Type={content_type})")
            return

        # Check file size from headers (if provided)
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_FILE_SIZE:
            print(f"⚠️ Skipping {url} (file too large: {content_length} bytes)")
            return

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename or "." not in filename:  # Generate safe default
            ext = content_type.split("/")[-1] or "jpg"
            filename = f"image_{uuid.uuid4().hex}.{ext}"

        filepath = os.path.join(FOLDER, filename)

        # Read content in chunks and compute hash
        file_data = b""
        for chunk in response.iter_content(8192):
            file_data += chunk
            if len(file_data) > MAX_FILE_SIZE:  # Double safety
                print(f"⚠️ Skipping {url} (exceeded size limit while downloading)")
                return

        file_hash = get_file_hash(file_data)
        if file_hash in downloaded_hashes:
            print(f"⚠️ Skipping {url} (duplicate image detected)")
            return

        # Save the file
        with open(filepath, "wb") as f:
            f.write(file_data)

        downloaded_hashes.add(file_hash)
        print(f"✅ Saved: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")


def main():
    urls = input("Enter image URLs (separated by spaces): ").strip().split()

    for url in urls:
        fetch_image(url)


if __name__ == "__main__":
    main()
print("Connection strengthened. Community enriched")