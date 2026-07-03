# Rikka GitHub Stats

Dynamic GitHub stats card generator with Rikka Takanashi anime theme. Beautiful, customizable SVG cards for your GitHub profile README.

## Features

- 🎨 **Rikka Takanashi theme** — Purple & teal color scheme inspired by the character
- 📊 **Real-time GitHub stats** — Repos, followers, following, join date
- 🚀 **Serverless** — Deployed on Vercel, zero VPS stress
- 🔗 **Embeddable SVG** — Direct image link, auto-updates

## Usage

Add to your GitHub profile README:

```markdown
![GitHub Stats](https://rikka-github-stats.vercel.app/api/stats?username=rikka0x)
```

Replace `rikka0x` with your GitHub username.

## Query Parameters

- `username` (required) — GitHub username
- `theme` (optional) — Theme variant (default: `rikka`)

Example:
```
https://rikka-github-stats.vercel.app/api/stats?username=rikka0x&theme=rikka
```

## Local Development

```bash
pip install -r requirements.txt
python -m http.server 3000
# Visit http://localhost:3000/api/stats?username=rikka0x
```

## Deploy to Vercel

1. Fork this repo
2. Go to [Vercel](https://vercel.com) → New Project
3. Import GitHub repo
4. Deploy
5. Your card is live at `https://<your-project>.vercel.app/api/stats?username=YOUR_USERNAME`

## Color Scheme

- **Background**: `#0f1419` (Dark)
- **Primary**: `#7c3aed` (Rikka Purple)
- **Accent**: `#14b8a6` (Teal)
- **Text**: `#e5e7eb` (Light Gray)

## License

MIT
