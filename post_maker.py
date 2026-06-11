#!/usr/bin/env python3
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Pillow 10 removed Image.ANTIALIAS; restore compatibility for older callers.
if not hasattr(Image, "ANTIALIAS"):
    try:
        Image.ANTIALIAS = Image.Resampling.LANCZOS
    except AttributeError:
        Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, VideoFileClip, afx

import config
from utils import pick_random_music


def make_post(video_path, quote):
    """Create a post: overlay quote text on video."""

    # Load video
    clip = VideoFileClip(str(video_path))

    # Limit to 30 seconds
    if clip.duration > 30:
        clip = clip.subclip(0, 30)

    # Resize if needed
    if clip.w > 720:
        clip = clip.resize(width=720)

    # Create text overlay
    overlay = _make_overlay(quote["text"], quote.get("author", "Unknown"), (clip.w, clip.h))
    overlay = overlay.set_duration(clip.duration)

    # Composite
    final = CompositeVideoClip([clip, overlay])

    # Attach background music from the music folder
    try:
        music_path = pick_random_music()
        music_clip = AudioFileClip(str(music_path)).subclip(0, clip.duration)
        if clip.audio:
            music_clip = music_clip.fx(afx.volumex, 0.3)
            final_audio = CompositeAudioClip([clip.audio, music_clip])
        else:
            final_audio = music_clip
        final = final.set_audio(final_audio)
    except FileNotFoundError:
        pass

    # Save
    output = config.OUTPUT_DIR / f"post_{int(Path(video_path).stat().st_mtime)}.mp4"
    final.write_videofile(
        str(output),
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset="fast",
        verbose=False,
        logger=None,
    )

    clip.close()
    final.close()
    return output


def _make_overlay(text, author, size):
    """Create a text overlay image with large centered text."""
    width, height = size

    wrapped_text = "\n".join(textwrap.wrap(f'"{text}"', width=22))
    wrapped_author = "\n".join(textwrap.wrap(f"— {author}", width=22))
    full_text = f"{wrapped_text}\n\n{wrapped_author}"

    try:
        font_size = max(40, min(width // 10, 90))
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    lines = full_text.split("\n")
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_heights.append(bbox[3] - bbox[1] + 12)
    total_height = sum(line_heights)

    y = (height - total_height) / 2
    for line, line_height in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        y += line_height

    return ImageClip(np.array(img))
