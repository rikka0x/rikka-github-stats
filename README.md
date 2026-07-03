# Rikka GitHub Stats

Custom GitHub stats card generator with anime theme. Self-hosted on Vercel, zero VPS stress.

![Preview](https://rikka-github-stats.vercel.app/api/stats?username=rikka0x&theme=rikka)

## Features

- **Custom anime theme** — Purple & teal color scheme (`#0d0b1a` / `#7c3aed` / `#14b8a6`)
- **GitHub avatar** — Inline base64 embed, no external dependency
- **Real-time stats** — Repos, followers, stars, forks, joined date
- **Progress bars** — Gradient bars for each stat
- **Serverless** — Python on Vercel, auto-deploy on push
- **Embeddable SVG** — Direct image link, 1hr cache

## Usage

Add to your GitHub profile README:

```markdown
![GitHub Stats](https://rikka-github-stats.vercel.app/api/stats?username=rikka0x)
```

Replace `rikka0x` with your GitHub username.

## Query Parameters

| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `username` | yes | — | GitHub username |
| `theme` | no | `rikka` | Theme variant (`rikka` or `dark`) |

Example:
```
https://rikka-github-stats.vercel.app/api/stats?username=rikka0x&theme=dark
```

## Themes

| Theme | Background | Primary | Accent |
|-------|-----------|---------|--------|
| `rikka` | `#0d0b1a` / `#1a1530` | `#7c3aed` (purple) | `#14b8a6` (teal) |
| `dark` | `#0d1117` / `#161b22` | `#58a6ff` (blue) | `#f778ba` (pink) |

## Deploy Your Own

1. Fork this repo
2. Go to [Vercel](https://vercel.com) → New Project → Import
3. Vercel auto-detects Python (no `vercel.json` needed)
4. Deploy — your card is live at `https://<your-project>.vercel.app/api/stats?username=YOUR_USERNAME`

### Requirements

- `pyproject.toml` with `[project]` table (PEP 621)
- `api/requirements.txt` — Vercel reads deps from here
- No Flask — uses `http.server.BaseHTTPRequestHandler` directly

## Tech

- Python 3.11+ serverless function
- GitHub REST API v3
- SVG with inline base64 avatar
- Vercel Python runtime (auto-detect, no config)

## License

MIT
