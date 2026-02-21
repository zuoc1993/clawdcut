"""Tests for stock tools."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from clawdcut.tools.stock_tools import (
    _format_freesound_audio,
    _format_pexels_photos,
    _format_pexels_videos,
    _format_pixabay_images,
    _format_pixabay_videos,
    create_stock_tools,
)

# --- Test Data ---

PEXELS_PHOTO_RESPONSE = {
    "photos": [
        {
            "id": 12345,
            "width": 1920,
            "height": 1080,
            "url": "https://www.pexels.com/photo/sunset-12345/",
            "photographer": "Test Photographer",
            "src": {
                "original": "https://images.pexels.com/photos/12345/original.jpeg",
                "large": "https://images.pexels.com/photos/12345/large.jpeg",
                "medium": "https://images.pexels.com/photos/12345/medium.jpeg",
            },
            "alt": "A beautiful sunset",
        }
    ],
    "total_results": 1,
    "page": 1,
    "per_page": 5,
}

PEXELS_VIDEO_RESPONSE = {
    "videos": [
        {
            "id": 67890,
            "width": 1920,
            "height": 1080,
            "url": "https://www.pexels.com/video/sunset-67890/",
            "duration": 15,
            "video_files": [
                {
                    "id": 111,
                    "quality": "hd",
                    "file_type": "video/mp4",
                    "width": 1920,
                    "height": 1080,
                    "link": "https://videos.pexels.com/67890-hd.mp4",
                },
                {
                    "id": 222,
                    "quality": "sd",
                    "file_type": "video/mp4",
                    "width": 640,
                    "height": 360,
                    "link": "https://videos.pexels.com/67890-sd.mp4",
                },
            ],
        }
    ],
    "total_results": 1,
    "page": 1,
    "per_page": 5,
}

PIXABAY_IMAGE_RESPONSE = {
    "total": 100,
    "totalHits": 500,
    "hits": [
        {
            "id": 11111,
            "pageURL": "https://pixabay.com/photos/sunset-11111/",
            "type": "photo",
            "tags": "sunset, nature, sky",
            "previewURL": "https://cdn.pixabay.com/photo/sunset_150.jpg",
            "webformatURL": "https://pixabay.com/get/sunset_640.jpg",
            "largeImageURL": "https://pixabay.com/get/sunset_1280.jpg",
            "imageWidth": 1920,
            "imageHeight": 1080,
            "downloads": 5000,
            "user": "TestUser",
        }
    ],
}

PIXABAY_VIDEO_RESPONSE = {
    "total": 50,
    "totalHits": 200,
    "hits": [
        {
            "id": 22222,
            "pageURL": "https://pixabay.com/videos/sunset-22222/",
            "type": "film",
            "tags": "sunset, nature",
            "duration": 20,
            "videos": {
                "large": {
                    "url": "https://cdn.pixabay.com/video/sunset_large.mp4",
                    "width": 1920,
                    "height": 1080,
                    "size": 12345678,
                },
                "medium": {
                    "url": "https://cdn.pixabay.com/video/sunset_medium.mp4",
                    "width": 1280,
                    "height": 720,
                    "size": 6789012,
                },
            },
            "user": "TestUser",
        }
    ],
}

FREESOUND_AUDIO_RESPONSE = {
    "count": 20,
    "results": [
        {
            "id": 33333,
            "name": "Cinematic Ambient Bed",
            "tags": ["cinematic", "ambient", "background"],
            "duration": 92,
            "username": "ComposerUser",
            "license": "Creative Commons 0",
            "previews": {
                "preview-hq-mp3": "https://cdn.freesound.org/previews/33333-hq.mp3",
            },
        }
    ],
}


# --- Fixtures ---


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    """Create a temporary working directory."""
    return tmp_path


@pytest.fixture
def tools(workdir: Path) -> dict:
    """Create stock tools bound to temp workdir, keyed by function name."""
    tool_list = create_stock_tools(workdir)
    return {fn.__name__: fn for fn in tool_list}


def _mock_response(
    data: dict | None = None, status_code: int = 200
) -> MagicMock:
    """Create a mock httpx Response."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = data or {}
    mock.raise_for_status.return_value = None
    mock.content = b"fake-binary-content"
    return mock


# --- Format Function Tests ---


class TestFormatPexelsPhotos:
    def test_formats_photo_results(self) -> None:
        result = _format_pexels_photos(PEXELS_PHOTO_RESPONSE)
        assert "12345" in result
        assert "A beautiful sunset" in result
        assert "Test Photographer" in result
        assert "1920" in result
        assert "1080" in result

    def test_empty_results(self) -> None:
        result = _format_pexels_photos({"photos": [], "total_results": 0})
        assert "No photos found" in result


class TestFormatPexelsVideos:
    def test_formats_video_results(self) -> None:
        result = _format_pexels_videos(PEXELS_VIDEO_RESPONSE)
        assert "67890" in result
        assert "15" in result
        assert "hd" in result

    def test_selects_best_quality_file(self) -> None:
        result = _format_pexels_videos(PEXELS_VIDEO_RESPONSE)
        assert "1920" in result
        assert "67890-hd.mp4" in result

    def test_empty_results(self) -> None:
        result = _format_pexels_videos({"videos": [], "total_results": 0})
        assert "No videos found" in result


class TestFormatPixabayImages:
    def test_formats_image_results(self) -> None:
        result = _format_pixabay_images(PIXABAY_IMAGE_RESPONSE)
        assert "11111" in result
        assert "sunset, nature, sky" in result
        assert "TestUser" in result
        assert "1920" in result

    def test_empty_results(self) -> None:
        result = _format_pixabay_images({"hits": [], "totalHits": 0})
        assert "No images found" in result


class TestFormatPixabayVideos:
    def test_formats_video_results(self) -> None:
        result = _format_pixabay_videos(PIXABAY_VIDEO_RESPONSE)
        assert "22222" in result
        assert "20" in result
        assert "TestUser" in result

    def test_empty_results(self) -> None:
        result = _format_pixabay_videos({"hits": [], "totalHits": 0})
        assert "No videos found" in result


class TestFormatFreesoundAudio:
    def test_formats_audio_results(self) -> None:
        result = _format_freesound_audio(FREESOUND_AUDIO_RESPONSE)
        assert "33333" in result
        assert "Cinematic Ambient Bed" in result
        assert "ComposerUser" in result
        assert "92" in result

    def test_empty_results(self) -> None:
        result = _format_freesound_audio({"results": [], "count": 0})
        assert "No audio found" in result


# --- Pexels Search Tests ---


class TestPexelsSearch:
    def test_search_photos(self, tools: dict, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(PEXELS_PHOTO_RESPONSE)
            result = tools["pexels_search"]("sunset")

        assert "12345" in result
        assert "A beautiful sunset" in result
        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        assert "v1/search" in call_url
        assert mock_get.call_args[1]["headers"]["Authorization"] == "test-key"

    def test_search_videos_uses_video_endpoint(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(PEXELS_VIDEO_RESPONSE)
            result = tools["pexels_search"]("sunset", media_type="video")

        assert "67890" in result
        call_url = mock_get.call_args[0][0]
        assert "videos/search" in call_url

    def test_missing_api_key(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("PEXELS_API_KEY", raising=False)
        result = tools["pexels_search"]("sunset")
        assert "PEXELS_API_KEY" in result

    def test_per_page_capped_at_15(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(PEXELS_PHOTO_RESPONSE)
            tools["pexels_search"]("sunset", per_page=50)

        params = mock_get.call_args[1]["params"]
        assert params["per_page"] <= 15

    def test_http_error_returns_error_message(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")
            result = tools["pexels_search"]("sunset")

        assert "Error" in result


# --- Pexels Download Tests ---


class TestPexelsDownload:
    def test_downloads_file(
        self,
        tools: dict,
        workdir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response()
            result = tools["pexels_download"](
                "https://example.com/photo.jpg",
                ".clawdcut/assets/images/photo.jpg",
            )

        target = workdir / ".clawdcut/assets/images/photo.jpg"
        assert target.exists()
        assert target.read_bytes() == b"fake-binary-content"
        assert str(target) in result

    def test_creates_parent_directories(
        self,
        tools: dict,
        workdir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response()
            tools["pexels_download"](
                "https://example.com/photo.jpg",
                ".clawdcut/assets/deep/nested/photo.jpg",
            )

        assert (workdir / ".clawdcut/assets/deep/nested/photo.jpg").exists()

    def test_http_error_returns_error_message(
        self,
        tools: dict,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("PEXELS_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")
            result = tools["pexels_download"](
                "https://example.com/photo.jpg",
                ".clawdcut/assets/images/photo.jpg",
            )

        assert "Error" in result


# --- Pixabay Search Tests ---


class TestPixabaySearch:
    def test_search_images(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PIXABAY_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(PIXABAY_IMAGE_RESPONSE)
            result = tools["pixabay_search"]("sunset")

        assert "11111" in result
        assert "sunset, nature, sky" in result
        params = mock_get.call_args[1]["params"]
        assert params["key"] == "test-key"
        assert params["q"] == "sunset"

    def test_search_videos_uses_video_endpoint(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PIXABAY_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(PIXABAY_VIDEO_RESPONSE)
            result = tools["pixabay_search"]("sunset", media_type="video")

        assert "22222" in result
        call_url = mock_get.call_args[0][0]
        assert "videos" in call_url

    def test_missing_api_key(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("PIXABAY_API_KEY", raising=False)
        result = tools["pixabay_search"]("sunset")
        assert "PIXABAY_API_KEY" in result

    def test_image_type_filter(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PIXABAY_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(PIXABAY_IMAGE_RESPONSE)
            tools["pixabay_search"]("sunset", media_type="illustration")

        params = mock_get.call_args[1]["params"]
        assert params["image_type"] == "illustration"

    def test_http_error_returns_error_message(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PIXABAY_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")
            result = tools["pixabay_search"]("sunset")

        assert "Error" in result


# --- Pixabay Download Tests ---


class TestPixabayDownload:
    def test_downloads_file(self, tools: dict, workdir: Path) -> None:
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response()
            result = tools["pixabay_download"](
                "https://cdn.pixabay.com/video/sunset.mp4",
                ".clawdcut/assets/videos/sunset.mp4",
            )

        target = workdir / ".clawdcut/assets/videos/sunset.mp4"
        assert target.exists()
        assert target.read_bytes() == b"fake-binary-content"
        assert str(target) in result

    def test_creates_parent_directories(self, tools: dict, workdir: Path) -> None:
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response()
            tools["pixabay_download"](
                "https://cdn.pixabay.com/photo/sunset.jpg",
                ".clawdcut/assets/deep/nested/sunset.jpg",
            )

        assert (workdir / ".clawdcut/assets/deep/nested/sunset.jpg").exists()


class TestFreesoundSearch:
    def test_search_audio(self, tools: dict, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("FREESOUND_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(FREESOUND_AUDIO_RESPONSE)
            result = tools["freesound_search"]("cinematic")

        assert "33333" in result
        params = mock_get.call_args[1]["params"]
        assert params["q"] == "cinematic"
        assert params["token"] == "test-key"
        assert "license" in params["filter"]

    def test_search_sfx_category(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("FREESOUND_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(FREESOUND_AUDIO_RESPONSE)
            tools["freesound_search"]("whoosh", category="sfx")

        params = mock_get.call_args[1]["params"]
        assert "tag:sfx" in params["filter"]

    def test_only_cc0_license(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("FREESOUND_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(FREESOUND_AUDIO_RESPONSE)
            tools["freesound_search"]("cinematic", license_type="cc0")

        params = mock_get.call_args[1]["params"]
        assert "Creative Commons 0" in params["filter"]
        assert "Attribution" not in params["filter"]

    def test_missing_api_key(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("FREESOUND_API_KEY", raising=False)
        result = tools["freesound_search"]("cinematic")
        assert "FREESOUND_API_KEY" in result

    def test_per_page_capped(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("FREESOUND_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response(FREESOUND_AUDIO_RESPONSE)
            tools["freesound_search"]("cinematic", per_page=100)

        params = mock_get.call_args[1]["params"]
        assert params["page_size"] <= 15

    def test_http_error_returns_error_message(
        self, tools: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("FREESOUND_API_KEY", "test-key")
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")
            result = tools["freesound_search"]("cinematic")

        assert "Error" in result


class TestFreesoundDownload:
    def test_downloads_file(self, tools: dict, workdir: Path) -> None:
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value = _mock_response()
            result = tools["freesound_download"](
                "https://cdn.freesound.org/previews/33333-hq.mp3",
                ".clawdcut/assets/audio/music/cinematic.mp3",
            )

        target = workdir / ".clawdcut/assets/audio/music/cinematic.mp3"
        assert target.exists()
        assert target.read_bytes() == b"fake-binary-content"
        assert str(target) in result

    def test_http_error_returns_error_message(self, tools: dict) -> None:
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")
            result = tools["freesound_download"](
                "https://cdn.freesound.org/previews/33333-hq.mp3",
                ".clawdcut/assets/audio/music/cinematic.mp3",
            )

        assert "Error" in result


# --- Factory Tests ---


class TestCreateStockTools:
    def test_returns_six_tools(self, workdir: Path) -> None:
        tools = create_stock_tools(workdir)
        assert len(tools) == 6

    def test_tool_names(self, workdir: Path) -> None:
        tools = create_stock_tools(workdir)
        names = [t.__name__ for t in tools]
        assert names == [
            "pexels_search",
            "pexels_download",
            "pixabay_search",
            "pixabay_download",
            "freesound_search",
            "freesound_download",
        ]

    def test_tools_have_docstrings(self, workdir: Path) -> None:
        tools = create_stock_tools(workdir)
        for tool in tools:
            assert tool.__doc__ is not None
            assert len(tool.__doc__) > 0
