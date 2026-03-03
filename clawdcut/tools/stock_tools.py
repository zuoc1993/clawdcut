"""Stock media API tools for searching and downloading free assets.

Supports Pexels and Pixabay for searching and downloading
free stock photos, videos, and other media.
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Callable

import httpx

PEXELS_PHOTO_URL = "https://api.pexels.com/v1/search"
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
PIXABAY_IMAGE_URL = "https://pixabay.com/api/"
PIXABAY_VIDEO_URL = "https://pixabay.com/api/videos/"
FREESOUND_SEARCH_URL = "https://freesound.org/apiv2/search/text/"
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 0.2


def _json_success(summary: str, **extra: Any) -> str:
    """Build a structured success payload."""
    return json.dumps(
        {
            "success": True,
            "summary": summary,
            **extra,
        },
        ensure_ascii=False,
    )


def _json_error(error: str, **extra: Any) -> str:
    """Build a structured error payload."""
    return json.dumps(
        {
            "success": False,
            "error": error,
            **extra,
        },
        ensure_ascii=False,
    )


def _is_retryable_http_error(error: httpx.HTTPError) -> bool:
    """Return whether the HTTP error should be retried."""
    if isinstance(error, httpx.HTTPStatusError):
        code = error.response.status_code
        return code >= 500 or code == 429
    return isinstance(error, httpx.RequestError)


def _request_with_retry(
    request_fn: Callable[..., httpx.Response],
    url: str,
    **kwargs: Any,
) -> httpx.Response:
    """Issue an HTTP request with bounded retries for transient failures."""
    last_error: httpx.HTTPError | None = None

    for attempt in range(MAX_RETRIES):
        try:
            response = request_fn(url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPError as error:
            last_error = error
            if not _is_retryable_http_error(error) or attempt == MAX_RETRIES - 1:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * (2**attempt))

    if last_error is not None:
        raise last_error
    raise RuntimeError("Unexpected retry loop exit without response.")


def _safe_target_path(workdir: Path, save_path: str) -> Path:
    """Resolve and validate save path under .clawdcut/assets/ only."""
    assets_root = (workdir / ".clawdcut" / "assets").resolve()
    target = (workdir / save_path).resolve()
    try:
        target.relative_to(assets_root)
    except ValueError as error:
        raise ValueError(
            "Error: invalid save_path; must be under .clawdcut/assets/"
        ) from error
    return target


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


def _format_freesound_audio(data: dict[str, Any]) -> str:
    """Format Freesound audio search results into readable text."""
    results = data.get("results", [])
    if not results:
        return "No audio found."

    total = data.get("count", 0)
    lines = [f"Found {total} audio tracks on Freesound (showing {len(results)}):\n"]

    for i, item in enumerate(results, 1):
        previews = item.get("previews", {})
        preview_url = previews.get("preview-hq-mp3", "N/A")
        lines.append(
            f"{i}. [ID: {item.get('id', '?')}] Name: {item.get('name', 'N/A')}\n"
            f"   User: {item.get('username', 'Unknown')}\n"
            f"   Duration: {item.get('duration', '?')}s\n"
            f"   License: {item.get('license', 'Unknown')}\n"
            f"   Preview URL: {preview_url}\n"
            f"   Download URL: {preview_url}"
        )

    return "\n".join(lines)


def create_stock_tools(workdir: Path) -> list[Callable[..., str]]:
    """Create stock media API tools bound to a working directory.

    Returns a list of tool callables:
    [
        pexels_search, pexels_download,
        pixabay_search, pixabay_download,
        freesound_search, freesound_download
    ]

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
            return _json_error(
                "Error: PEXELS_API_KEY environment variable is not set.",
                provider="pexels",
                operation="search",
            )

        headers = {"Authorization": api_key}
        url = PEXELS_VIDEO_URL if media_type == "video" else PEXELS_PHOTO_URL
        params: dict[str, str | int] = {
            "query": query,
            "per_page": min(max(per_page, 1), 15),
        }

        try:
            data = _request_with_retry(
                httpx.get, url, headers=headers, params=params, timeout=30.0
            ).json()
        except httpx.HTTPError as e:
            return _json_error(
                f"Error searching Pexels: {e}",
                provider="pexels",
                operation="search",
            )

        summary = (
            _format_pexels_videos(data)
            if media_type == "video"
            else _format_pexels_photos(data)
        )
        return _json_success(
            summary,
            provider="pexels",
            operation="search",
            media_type=media_type,
            raw_count=(
                len(data.get("videos", []))
                if media_type == "video"
                else len(data.get("photos", []))
            ),
        )

    def pexels_download(url: str, save_path: str) -> str:
        """Download a media file from Pexels to the local filesystem.

        Args:
            url: Download URL from pexels_search results.
            save_path: Relative path to save the file
                (e.g. .clawdcut/assets/images/sunset.jpg).

        Returns:
            The local file path where the file was saved.
        """
        try:
            target = _safe_target_path(workdir, save_path)
        except ValueError as error:
            return _json_error(
                str(error),
                provider="pexels",
                operation="download",
            )
        target.parent.mkdir(parents=True, exist_ok=True)

        api_key = os.environ.get("PEXELS_API_KEY", "")
        headers = {"Authorization": api_key} if api_key else {}

        try:
            resp = _request_with_retry(
                httpx.get,
                url,
                headers=headers,
                follow_redirects=True,
                timeout=60.0,
            )
            target.write_bytes(resp.content)
        except httpx.HTTPError as e:
            return _json_error(
                f"Error downloading from Pexels: {e}",
                provider="pexels",
                operation="download",
            )

        return _json_success(
            f"Downloaded to: {target}",
            provider="pexels",
            operation="download",
            path=str(target),
        )

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
            return _json_error(
                "Error: PIXABAY_API_KEY environment variable is not set.",
                provider="pixabay",
                operation="search",
            )

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
            data = _request_with_retry(
                httpx.get, url, params=params, timeout=30.0
            ).json()
        except httpx.HTTPError as e:
            return _json_error(
                f"Error searching Pixabay: {e}",
                provider="pixabay",
                operation="search",
            )

        summary = (
            _format_pixabay_videos(data)
            if is_video
            else _format_pixabay_images(data)
        )
        return _json_success(
            summary,
            provider="pixabay",
            operation="search",
            media_type=media_type,
            raw_count=len(data.get("hits", [])),
        )

    def pixabay_download(url: str, save_path: str) -> str:
        """Download a media file from Pixabay to the local filesystem.

        Args:
            url: Download URL from pixabay_search results.
            save_path: Relative path to save the file
                (e.g. .clawdcut/assets/videos/nature.mp4).

        Returns:
            The local file path where the file was saved.
        """
        try:
            target = _safe_target_path(workdir, save_path)
        except ValueError as error:
            return _json_error(
                str(error),
                provider="pixabay",
                operation="download",
            )
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            resp = _request_with_retry(
                httpx.get,
                url,
                follow_redirects=True,
                timeout=60.0,
            )
            target.write_bytes(resp.content)
        except httpx.HTTPError as e:
            return _json_error(
                f"Error downloading from Pixabay: {e}",
                provider="pixabay",
                operation="download",
            )

        return _json_success(
            f"Downloaded to: {target}",
            provider="pixabay",
            operation="download",
            path=str(target),
        )

    def freesound_search(
        query: str,
        category: str = "music",
        license_type: str = "cc0+attribution",
        per_page: int = 10,
    ) -> str:
        """Search Freesound for free music or sound effects.

        Args:
            query: Search keywords (English recommended for broader results).
            category: Audio category - "music" or "sfx".
            license_type: "cc0" or "cc0+attribution".
            per_page: Number of results to return (1-15).

        Returns:
            Formatted search results with id, name, duration, preview URL,
            and download URL.
        """
        api_key = os.environ.get("FREESOUND_API_KEY", "")
        if not api_key:
            return _json_error(
                "Error: FREESOUND_API_KEY environment variable is not set.",
                provider="freesound",
                operation="search",
            )

        category_filter = "tag:sfx" if category == "sfx" else "tag:music"
        if license_type == "cc0":
            license_filter = 'license:"Creative Commons 0"'
        else:
            license_filter = (
                'license:"Creative Commons 0" OR license:Attribution'
            )
        params: dict[str, str | int] = {
            "token": api_key,
            "q": query,
            "page_size": min(max(per_page, 1), 15),
            "fields": "id,name,username,duration,license,previews",
            "filter": f"({license_filter}) {category_filter}",
        }

        try:
            data = _request_with_retry(
                httpx.get, FREESOUND_SEARCH_URL, params=params, timeout=30.0
            ).json()
        except httpx.HTTPError as e:
            return _json_error(
                f"Error searching Freesound: {e}",
                provider="freesound",
                operation="search",
            )

        return _json_success(
            _format_freesound_audio(data),
            provider="freesound",
            operation="search",
            media_type=category,
            raw_count=len(data.get("results", [])),
        )

    def freesound_download(url: str, save_path: str) -> str:
        """Download an audio file from Freesound to local filesystem.

        Args:
            url: Download URL from freesound_search results.
            save_path: Relative save path
                (e.g. .clawdcut/assets/audio/music/theme.mp3).

        Returns:
            The local file path where the file was saved.
        """
        try:
            target = _safe_target_path(workdir, save_path)
        except ValueError as error:
            return _json_error(
                str(error),
                provider="freesound",
                operation="download",
            )
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            resp = _request_with_retry(
                httpx.get,
                url,
                follow_redirects=True,
                timeout=60.0,
            )
            target.write_bytes(resp.content)
        except httpx.HTTPError as e:
            return _json_error(
                f"Error downloading from Freesound: {e}",
                provider="freesound",
                operation="download",
            )

        return _json_success(
            f"Downloaded to: {target}",
            provider="freesound",
            operation="download",
            path=str(target),
        )

    return [
        pexels_search,
        pexels_download,
        pixabay_search,
        pixabay_download,
        freesound_search,
        freesound_download,
    ]
