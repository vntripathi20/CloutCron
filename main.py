#!/usr/bin/env python3
import sys

import config
from post_maker import make_post
from uploader import post_to_instagram
from utils import setup, load_quotes, pick_random_video, log_it


def main():
    setup()

    # Check Instagram credentials
    if not config.IG_USER or not config.IG_PASS:
        print("ERROR: Set IG_USER and IG_PASS environment variables")
        sys.exit(1)

    try:
        # Get a random quote
        quotes = load_quotes()
        if not quotes:
            raise Exception("No quotes in data/quotes.json")
        import random
        quote = random.choice(quotes)

        # Pick a video
        video = pick_random_video()

        # Make the post (overlay quote on video)
        output_file = make_post(video, quote)
        print(f"Generated: {output_file}")

        # Upload to Instagram
        caption = f"💡 {quote['text']} — {quote.get('author', 'Unknown')}\n\n#CloutCron #automation #python"
        post_to_instagram(str(output_file), caption, config.IG_USER, config.IG_PASS)

        log_it(quote["text"], str(output_file), "SUCCESS")
        print("Posted!")

    except Exception as e:
        print(f"Error: {e}")
        log_it("unknown", "unknown", f"FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
