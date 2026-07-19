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

## Going live (GitHub Pages)
The workflow now deploys automatically to GitHub Pages on every push to `main`.
One-time setup after your first push:
1. Go to your repo → **Settings → Pages**
2. Under "Build and deployment", set **Source** to **GitHub Actions**
3. Push to `main` — the workflow builds, verifies the DB, and deploys the game

Your live URL will be `https://<your-username>.github.io/<repo-name>/`
(shown in the Actions run summary and under Settings → Pages once deployed).

## Installing on Android (as a real app)
This game is a PWA (Progressive Web App) — no Play Store needed.

1. Open your live GitHub Pages URL in **Chrome** on your Android phone
2. Tap the **⋮** menu → **Install app** (or **Add to Home screen**)
3. Confirm — an app icon appears on your home screen
4. Open it from there: it launches fullscreen, no browser bar, and works offline

Note: your repo must be **Public** for GitHub Pages' free tier to serve it
(private repos need GitHub Pro/Team/Enterprise for Pages).
