# CloutCron

A simple Raspberry Pi automation project that generates and posts Instagram content daily.

Built over a weekend for fun. Just a few Python scripts—no complexity.

## How it works

1. **main.py** — orchestrates everything
2. **post_maker.py** — overlays a quote on a random video
3. **uploader.py** — posts to Instagram
4. **utils.py** — helpers (load quotes, pick videos, logging)
5. **config.py** — paths and env settings

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set Instagram credentials on Linux/macOS
export IG_USER="your_username"
export IG_PASS="your_password"

# Add at least one video to videos/
cp /path/to/video.mp4 videos/

# Add optional music tracks to music/
cp /path/to/song.mp3 music/

# Run once
python3 main.py
```

If you are on Windows PowerShell:

```powershell
$env:IG_USER = "your_username"
$env:IG_PASS = "your_password"
python main.py
```

If you are on Windows cmd.exe:

```cmd
set IG_USER=your_username
set IG_PASS=your_password
python main.py
```

## Cron job (Raspberry Pi)

Add to crontab to run daily at 9 AM:

```
0 9 * * * cd /home/pi/CloutCron && python3 main.py
```

## Project structure

```
CloutCron/
├── main.py              # main orchestrator
├── post_maker.py        # overlay quote on video
├── uploader.py          # post to Instagram
├── utils.py             # helpers
├── config.py            # config
├── requirements.txt
├── data/
│   └── quotes.json      # quote list
├── videos/              # add your background videos here
├── music/               # add music tracks here
├── output/              # generated posts
└── logs/
    └── posts.log        # posting history
```

## quotes.json format

```json
[
  {
    "text": "The best time to plant a tree was 20 years ago. The second best time is now.",
    "author": "Chinese Proverb"
  },
  {
    "text": "Keep it simple. Keep it fun.",
    "author": "You"
  }
]
```

## That's it

Set credentials, add videos, add quotes, run. Posts daily. Logs everything.

No dashboard, no complexity. Just pure hacker vibes.
