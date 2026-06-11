#!/usr/bin/env python3
from pathlib import Path

from instagrapi import Client


def post_to_instagram(media_path, caption, username, password):
    """Upload to Instagram."""
    client = Client()

    # Try to load cached session
    session_file = Path.cwd() / ".ig_session"
    if session_file.exists():
        try:
            client.load_settings(str(session_file))
        except:
            pass

    # Login if needed
    authenticated = None
    if hasattr(client, "is_authenticated"):
        authenticated = client.is_authenticated
    elif hasattr(client, "authenticated"):
        authenticated = client.authenticated
    elif hasattr(client, "login_required"):
        try:
            authenticated = not client.login_required()
        except Exception:
            authenticated = None

    if not authenticated:
        print(f"Logging in as {username}...")
        client.login(username, password)
        client.dump_settings(str(session_file))

    # Upload
    ext = Path(media_path).suffix.lower()
    if ext == ".mp4":
        print("Uploading video...")
        client.video_upload(media_path, caption=caption)
    else:
        print("Uploading photo...")
        client.photo_upload(media_path, caption=caption)

    print("Done!")
