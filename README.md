# Nokia Snake

A classic Nokia-style Snake game (VIKRAM edition), playable in-browser.

## Structure
- `index.html` — the game itself (open directly in a browser or serve via GitHub Pages)
- `build.py` — self-loading build script: auto-creates and verifies the SQLite
  leaderboard database (`db/scores.db`) on every run, safe to re-run anytime
- `.github/workflows/build.yml` — GitHub Actions workflow that runs `build.py`
  automatically on every push/PR

## Run locally
```bash
python3 build.py   # sets up db/scores.db
open index.html    # or just double-click it
```
