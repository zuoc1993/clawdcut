"""Stock media API tools for searching and downloading free assets.

Supports Pexels and Pixabay for searching and downloading
free stock photos, videos, and other media.
"""

import os
from pathlib import Path
from typing import Any, Callable

import httpx

PEXELS_PHOTO_URL = "https://api.pexels.com/v1/search"
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
PIXABAY_IMAGE_URL = "https://pixabay.com/api/"
PIXABAY_VIDEO_URL = "https://pixabay.com/api/videos/"


def _format_pexels_photos(data: dict[str, Any]) -> str:
    """Format Pexels photo search results into readable text."""
    photos = data.get("photos", [])
    if not photos:
        return "No photos found."

    total = data.get("total_results", 0)
    lines = [f"Found {total} photos on Pexels (showing {len(photos)}):\n"]

    for i, photo in enumerate(photos, 1):
        src = photo.get("src", {})
        lines.append(
            f"{i}. [ID: {photo['id']}] \"{photo.get('alt', 'No description')}\"\n"
            f"   Photographer: {photo.get('photographer', 'Unknown')}\n"
            f"   Resolution: {photo.get('width', '?')}x{photo.get('height', '?')}\n"
            f"   Preview: {src.get('medium', 'N/A')}\n"
            f"   Download URL: {src.get('original', 'N/A')}"
        )

    return "\n".join(lines)


def _format_pexels_videos(data: dict[str, Any]) -> str:
    """Format Pexels video search results into readable text."""
    videos = data.get("videos", [])
    if not videos:
        return "No videos found."

    total = data.get("total_results", 0)
    lines = [f"Found {total} videos on Pexels (showing {len(videos)}):\n"]

    for i, video in enumerate(videos, 1):
        video_files = video.get("video_files", [])
        best = (
            max(video_files, key=lambda f: f.get("width", 0)) if video_files else {}
        )
        lines.append(
            f"{i}. [ID: {video['id']}] Duration: {video.get('duration', '?')}s\n"
            f"   Resolution: {best.get('width', '?')}x{best.get('height', '?')}\n"
            f"   Quality: {best.get('quality', '?')}\n"
            f"   Download URL: {best.get('link', 'N/A')}"
        )

    return "\n".join(lines)


def _format_pixabay_images(data: dict[str, Any]) -> str:
    """Format Pixabay image search results into readable text."""
    hits = data.get("hits", [])
    if not hits:
        return "No images found."

    total = data.get("totalHits", 0)
    lines = [f"Found {total} images on Pixabay (showing {len(hits)}):\n"]

    for i, hit in enumerate(hits, 1):
        lines.append(
            f"{i}. [ID: {hit['id']}] Tags: {hit.get('tags', 'N/A')}\n"
            f"   User: {hit.get('user', 'Unknown')}\n"
            f"   Resolution: {hit.get('imageWidth', '?')}x"
            f"{hit.get('imageHeight', '?')}\n"
            f"   Downloads: {hit.get('downloads', 0)}\n"
            f"   Preview: {hit.get('webformatURL', 'N/A')}\n"
            f"   Download URL: {hit.get('largeImageURL', 'N/A')}"
        )

    return "\n".join(lines)


def _format_pixabay_videos(data: dict[str, Any]) -> str:
    """Format Pixabay video search results into readable text."""
    hits = data.get("hits", [])
    if not hits:
        return "No videos found."

    total = data.get("totalHits", 0)
    lines = [f"Found {total} videos on Pixabay (showing {len(hits)}):\n"]

    for i, hit in enumerate(hits, 1):
        videos = hit.get("videos", {})
        large = videos.get("large", {})
        lines.append(
            f"{i}. [ID: {hit['id']}] Tags: {hit.get('tags', 'N/A')}\n"
            f"   User: {hit.get('user', 'Unknown')}\n"
            f"   Duration: {hit.get('duration', '?')}s\n"
            f"   Resolution: {large.get('width', '?')}x{large.get('height', '?')}\n"
            f"   Download URL: {large.get('url', 'N/A')}"
        )

    return "\n".join(lines)


def create_stock_tools(workdir: Path) -> list[Callable[..., str]]:
    """Create stock media API tools bound to a working directory.

    Returns a list of tool callables:
    [pexels_search, pexels_download, pixabay_search, pixabay_download]

    Args:
        workdir: Working directory for resolving relative save paths.
    """

    def pexels_search(
        query: str,
        media_type: str = "photo",
        per_page: int = 5,
    ) -> str:
        """Search Pexels for free stock photos or videos.

        Args:
            query: Search keywords (English recommended for broader results).
            media_type: Type of media - "photo" or "video".
            per_page: Number of results to return (1-15).

        Returns:
            Formatted search results with id, description, preview URL,
            download URL, and resolution.
        """
        api_key = os.environ.get("PEXELS_API_KEY", "")
        if not api_key:
            return "Error: PEXELS_API_KEY environment variable is not set."

        headers = {"Authorization": api_key}
        url = PEXELS_VIDEO_URL if media_type == "video" else PEXELS_PHOTO_URL
        params: dict[str, str | int] = {
            "query": query,
            "per_page": min(max(per_page, 1), 15),
        }

        try:
            resp = httpx.get(url, headers=headers, params=params, timeout=30.0)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as e:
            return f"Error searching Pexels: {e}"

        if media_type == "video":
            return _format_pexels_videos(data)
        return _format_pexels_photos(data)

    def pexels_download(url: str, save_path: str) -> str:
        """Download a media file from Pexels to the local filesystem.

        Args:
            url: Download URL from pexels_search results.
            save_path: Relative path to save the file
                (e.g. .clawdcut/assets/images/sunset.jpg).

        Returns:
            The local file path where the file was saved.
        """
        target = workdir / save_path
        target.parent.mkdir(parents=True, exist_ok=True)

        api_key = os.environ.get("PEXELS_API_KEY", "")
        headers = {"Authorization": api_key} if api_key else {}

        try:
            resp = httpx.get(
                url, headers=headers, follow_redirects=True, timeout=60.0
            )
            resp.raise_for_status()
            target.write_bytes(resp.content)
        except httpx.HTTPError as e:
            return f"Error downloading from Pexels: {e}"

        return f"Downloaded to: {target}"

    def pixabay_search(
        query: str,
        media_type: str = "photo",
        per_page: int = 5,
    ) -> str:
        """Search Pixabay for free stock images or videos.

        Args:
            query: Search keywords (English recommended for broader results).
            media_type: Type of media - "photo", "illustration",
                "vector", or "video".
            per_page: Number of results to return (3-15).

        Returns:
            Formatted search results with id, tags, preview URL,
            download URL, and resolution.
        """
        api_key = os.environ.get("PIXABAY_API_KEY", "")
        if not api_key:
            return "Error: PIXABAY_API_KEY environment variable is not set."

        is_video = media_type == "video"
        url = PIXABAY_VIDEO_URL if is_video else PIXABAY_IMAGE_URL
        params: dict[str, str | int] = {
            "key": api_key,
            "q": query,
            "per_page": min(max(per_page, 3), 15),
        }
        if not is_video and media_type in ("photo", "illustration", "vector"):
            params["image_type"] = media_type

        try:
            resp = httpx.get(url, params=params, timeout=30.0)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as e:
            return f"Error searching Pixabay: {e}"

        if is_video:
            return _format_pixabay_videos(data)
        return _format_pixabay_images(data)

    def pixabay_download(url: str, save_path: str) -> str:
        """Download a media file from Pixabay to the local filesystem.

        Args:
            url: Download URL from pixabay_search results.
            save_path: Relative path to save the file
                (e.g. .clawdcut/assets/videos/nature.mp4).

        Returns:
            The local file path where the file was saved.
        """
        target = workdir / save_path
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            resp = httpx.get(url, follow_redirects=True, timeout=60.0)
            resp.raise_for_status()
            target.write_bytes(resp.content)
        except httpx.HTTPError as e:
            return f"Error downloading from Pixabay: {e}"

        return f"Downloaded to: {target}"

    return [pexels_search, pexels_download, pixabay_search, pixabay_download]
