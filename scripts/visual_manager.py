#!/usr/bin/env python3
"""
EvansMathibe Agency - Visual Assets Manager
Handles images, videos, and visual content processing
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

AGENCY_ROOT = Path("/home/ev/EvansMathibe_Agency")
ASSETS_DIR = AGENCY_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
VIDEOS_DIR = ASSETS_DIR / "videos"
GALLERIES_DIR = ASSETS_DIR / "galleries"

for d in [ASSETS_DIR, IMAGES_DIR, VIDEOS_DIR, GALLERIES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"]
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mov", ".avi", ".mkv", ".webm"]


class VisualAssetsManager:
    def __init__(self):
        self.assets_index = self._load_index()

    def _load_index(self) -> Dict:
        index_file = ASSETS_DIR / "index.json"
        if index_file.exists():
            with open(index_file) as f:
                return json.load(f)
        return {"images": [], "videos": [], "galleries": [], "last_updated": None}

    def _save_index(self):
        self.assets_index["last_updated"] = datetime.now().isoformat()
        with open(ASSETS_DIR / "index.json", "w") as f:
            json.dump(self.assets_index, f, indent=2)

    def scan_directory(self, directory: Path):
        images_found = []
        videos_found = []

        for ext in SUPPORTED_IMAGE_FORMATS:
            images_found.extend(list(directory.glob(f"*{ext}")))
            images_found.extend(list(directory.glob(f"*{ext.upper()}")))

        for ext in SUPPORTED_VIDEO_FORMATS:
            videos_found.extend(list(directory.glob(f"*{ext}")))
            videos_found.extend(list(directory.glob(f"*{ext.upper()}")))

        return images_found, videos_found

    def optimize_image(
        self, input_path: str, output_path: str = None, quality: int = 85
    ):
        input_file = Path(input_path)
        if not input_file.exists():
            return {"error": "File not found"}

        output_file = Path(output_path) if output_path else input_file
        ext = input_file.suffix.lower()

        if ext == ".gif":
            return {"status": "skipped", "reason": "GIF optimization not supported"}

        try:
            cmd = [
                "convert",
                str(input_file),
                "-quality",
                str(quality),
                str(output_file),
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {
                "status": "success",
                "input": str(input_file),
                "output": str(output_file),
            }
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def create_thumbnail(
        self, input_path: str, output_path: str, size: str = "400x300"
    ):
        try:
            cmd = [
                "convert",
                str(input_path),
                "-thumbnail",
                size + "^",
                "-gravity",
                "center",
                "-extent",
                size,
                str(output_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "thumbnail": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def create_video_thumbnail(
        self, video_path: str, output_path: str, timestamp: str = "00:00:01"
    ):
        try:
            cmd = [
                "ffmpeg",
                "-i",
                str(video_path),
                "-ss",
                timestamp,
                "-vframes",
                "1",
                str(output_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "thumbnail": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def convert_video(self, input_path: str, output_path: str, codec: str = "libx264"):
        try:
            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-c:v",
                codec,
                "-preset",
                "fast",
                str(output_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "output": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def create_gallery(self, name: str, image_paths: List[str], layout: str = "grid"):
        gallery_data = {
            "name": name,
            "layout": layout,
            "images": [str(p) for p in image_paths],
            "created": datetime.now().isoformat(),
        }

        gallery_file = GALLERIES_DIR / f"{name.lower().replace(' ', '_')}.json"
        with open(gallery_file, "w") as f:
            json.dump(gallery_data, f, indent=2)

        self.assets_index["galleries"].append(str(gallery_file))
        self._save_index()

        return {
            "status": "success",
            "gallery": str(gallery_file),
            "images": len(image_paths),
        }

    def get_asset_info(self, file_path: str) -> Dict:
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}

        info = {
            "name": path.name,
            "extension": path.suffix.lower(),
            "size": path.stat().st_size,
            "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
        }

        if path.suffix.lower() in SUPPORTED_IMAGE_FORMATS:
            try:
                result = subprocess.run(
                    ["identify", "-format", "%wx%h", str(path)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                info["dimensions"] = result.stdout.strip()
            except:
                pass

        return info

    def list_assets(self, asset_type: str = "all") -> Dict:
        if asset_type in ["all", "images"]:
            images, _ = self.scan_directory(IMAGES_DIR)
            self.assets_index["images"] = [str(p) for p in images]

        if asset_type in ["all", "videos"]:
            _, videos = self.scan_directory(VIDEOS_DIR)
            self.assets_index["videos"] = [str(p) for p in videos]

        self._save_index()

        return {
            "images": self.assets_index["images"],
            "videos": self.assets_index["videos"],
            "galleries": self.assets_index["galleries"],
        }


def main():
    import sys

    manager = VisualAssetsManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            assets = manager.list_assets()
            print(json.dumps(assets, indent=2))

        elif command == "scan":
            path = sys.argv[2] if len(sys.argv) > 2 else "."
            images, videos = manager.scan_directory(Path(path))
            print(f"Found {len(images)} images and {len(videos)} videos")

        elif command == "info" and len(sys.argv) > 2:
            info = manager.get_asset_info(sys.argv[2])
            print(json.dumps(info, indent=2))

        elif command == "gallery" and len(sys.argv) > 2:
            name = sys.argv[2]
            images = sys.argv[3:] if len(sys.argv) > 3 else []
            if images:
                result = manager.create_gallery(name, images)
                print(json.dumps(result, indent=2))
            else:
                print(
                    "Usage: python visual_manager.py gallery <name> <image1> <image2> ..."
                )

        elif command == "thumbnail" and len(sys.argv) > 3:
            result = manager.create_thumbnail(sys.argv[2], sys.argv[3])
            print(json.dumps(result, indent=2))

    else:
        print("EvansMathibe Visual Assets Manager")
        print("=" * 45)
        print("Commands:")
        print("  python visual_manager.py list                    - List all assets")
        print(
            "  python visual_manager.py scan <path>             - Scan directory for assets"
        )
        print("  python visual_manager.py info <file>              - Get asset info")
        print("  python visual_manager.py gallery <name> <imgs>   - Create gallery")
        print("  python visual_manager.py thumbnail <in> <out>    - Create thumbnail")


if __name__ == "__main__":
    main()
