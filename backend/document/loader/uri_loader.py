# document/loader/uri_loader.py
from .base import BaseLoader
import httpx
from bs4 import BeautifulSoup

class UriLoader(BaseLoader):
    def load_file(self, uri: str) -> str:
        """
        Fetches the content from the URI.
        If it's HTML, extracts readable text.
        """
        # Fetch content
        response = httpx.get(uri, timeout=10.0)
        response.raise_for_status()  # Raise error if status != 200
        content_type = response.headers.get("Content-Type", "")

        if "text/html" in content_type:
            # Parse HTML to text
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract visible text
            text = soup.get_text(separator="\n")
            return text
        else:
            # For plain text or other content types
            return response.text