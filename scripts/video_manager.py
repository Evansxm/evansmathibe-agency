#!/usr/bin/env python3
"""
EvansMathibe Agency - Video Manager Agent
Handles video processing, optimization, and deployment for the website
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime

AGENCY_ROOT = Path("/home/ev/EvansMathibe_Agency")
VIDEOS_DIR = AGENCY_ROOT / "website" / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB GitHub Pages limit


class VideoManager:
    def __init__(self):
        self.videos = self._scan_videos()

    def _scan_videos(self):
        videos = []
        for ext in [".mp4", ".webm", ".ogg", ".mov"]:
            for v in VIDEOS_DIR.glob(f"*{ext}"):
                videos.append(
                    {
                        "name": v.name,
                        "path": str(v),
                        "size": v.stat().st_size,
                        "size_mb": round(v.stat().st_size / (1024 * 1024), 2),
                    }
                )
        return videos

    def add_video(self, video_path):
        src = Path(video_path)
        if not src.exists():
            return {"error": "File not found"}

        size_mb = src.stat().st_size / (1024 * 1024)
        if size_mb > 100:
            return {"error": f"File too large: {size_mb}MB. Max 100MB for GitHub Pages"}

        dst = VIDEOS_DIR / src.name
        import shutil

        shutil.copy2(src, dst)

        return {"status": "success", "video": dst.name, "size_mb": round(size_mb, 2)}

    def compress_video(self, input_path, output_path=None, quality="medium"):
        """Compress video for web"""
        if output_path is None:
            input_path = Path(input_path)
            output_path = input_path.stem + "_compressed.mp4"

        # Quality presets
        crf_values = {"high": 23, "medium": 28, "low": 32}
        crf = crf_values.get(quality, 28)

        cmd = [
            "ffmpeg",
            "-i",
            str(input_path),
            "-vcodec",
            "libx264",
            "-crf",
            str(crf),
            "-preset",
            "fast",
            "-acodec",
            "aac",
            "-movflags",
            "+faststart",
            str(output_path),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "output": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def create_thumbnail(self, video_path, output_path, timestamp="00:00:01"):
        cmd = [
            "ffmpeg",
            "-i",
            str(video_path),
            "-ss",
            timestamp,
            "-vframes",
            "1",
            "-s",
            "320x180",
            str(output_path),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "thumbnail": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def get_video_info(self, video_path):
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except:
            return {"error": "Could not get video info"}

    def list_videos(self):
        return self.videos

    def get_html_embed_code(self, video_name, autoplay=True):
        base_url = "videos"
        code = f'''<video {"autoplay" if autoplay else ""} loop muted playsinline controls style="width:100%;border-radius:10px;">
    <source src="{base_url}/{video_name}" type="video/mp4">
    Your browser does not support the video tag.
</video>'''
        return code


def main():
    import sys

    manager = VideoManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            videos = manager.list_videos()
            print(f"\nVideos in repository: {len(videos)}")
            for v in videos:
                print(f"  - {v['name']} ({v['size_mb']}MB)")

        elif command == "add" and len(sys.argv) > 2:
            result = manager.add_video(sys.argv[2])
            print(json.dumps(result, indent=2))

        elif command == "compress" and len(sys.argv) > 2:
            quality = sys.argv[3] if len(sys.argv) > 3 else "medium"
            result = manager.compress_video(sys.argv[2], quality=quality)
            print(json.dumps(result, indent=2))

        elif command == "info" and len(sys.argv) > 2:
            info = manager.get_video_info(sys.argv[2])
            print(json.dumps(info, indent=2))

        elif command == "code" and len(sys.argv) > 2:
            code = manager.get_html_embed_code(sys.argv[2])
            print(code)

        else:
            print("Video Manager Commands:")
            print("  python video_manager.py list")
            print("  python video_manager.py add <video_path>")
            print("  python video_manager.py compress <video_path> [quality]")
            print("  python video_manager.py info <video_path>")
            print("  python video_manager.py code <video_name>")
    else:
        videos = manager.list_videos()
        print(f"Videos: {len(videos)} found")
        print(f"Directory: {VIDEOS_DIR}")


if __name__ == "__main__":
    main()
