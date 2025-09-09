import os
import requests
from urllib.parse import urlparse
import uuid

def fetch_image():
    # Prompt user for URL
    url = input("Enter the image URL: ").strip()

    # Create directory if it doesn't exist
    folder = "Fetched_Images"
    os.makedirs(folder, exist_ok=True)

    try:
        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename:  # If no filename, generate a unique one
            filename = f"image_{uuid.uuid4().hex}.jpg"

        filepath = os.path.join(folder, filename)

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✅ Image saved successfully as {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch image: {e}")

if __name__ == "__main__":
    fetch_image()
