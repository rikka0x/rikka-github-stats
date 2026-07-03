import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            username = params.get('username', ['rikka0x'])[0]
            theme = params.get('theme', ['rikka'])[0]
            
            # Fetch GitHub user data
            headers = {'Accept': 'application/vnd.github.v3+json'}
            if os.environ.get('GITHUB_TOKEN'):
                headers['Authorization'] = f'token {os.environ["GITHUB_TOKEN"]}'
            
            resp = requests.get(f'https://api.github.com/users/{username}', timeout=10, headers=headers)
            if resp.status_code != 200:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'User not found')
                return
            
            user = resp.json()
            repos_count = user.get('public_repos', 0)
            followers = user.get('followers', 0)
            following = user.get('following', 0)
            created_at = user.get('created_at', '').split('T')[0]
            display_name = user.get('name', username) or username
            avatar_url = user.get('avatar_url', '')
            
            # Fetch repos for stars/forks
            stars_total = 0
            forks_total = 0
            commits_total = 0
            try:
                repos_resp = requests.get(
                    f'https://api.github.com/users/{username}/repos?per_page=100&sort=pushed',
                    timeout=10, headers=headers
                )
                if repos_resp.status_code == 200:
                    for repo in repos_resp.json():
                        stars_total += repo.get('stargazers_count', 0)
                        forks_total += repo.get('forks_count', 0)
            except:
                pass
            
            # Theme presets
            themes = {
                'rikka': {
                    'bg': '#0d0b1a', 'bg2': '#1a1530',
                    'border': '#7c3aed', 'title': '#a78bfa',
                    'text': '#e2e8f0', 'subtext': '#94a3b8',
                    'accent': '#14b8a6', 'accent2': '#ec4899',
                    'gold': '#fbbf24'
                },
                'dark': {
                    'bg': '#0d1117', 'bg2': '#161b22',
                    'border': '#30363d', 'title': '#58a6ff',
                    'text': '#c9d1d9', 'subtext': '#8b949e',
                    'accent': '#58a6ff', 'accent2': '#f778ba',
                    'gold': '#d29922'
                }
            }
            t = themes.get(theme, themes['rikka'])
            
            def esc(s):
                return str(s).replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"')
            
            # Progress bar widths
            bar_max = 200
            def bar_width(val, scale):
                return min(val / scale * bar_max, bar_max)
            
            # Fetch avatar from GitHub and convert to base64
            import base64
            avatar_b64 = ''
            try:
                av_resp = requests.get(avatar_url, timeout=10)
                if av_resp.status_code == 200:
                    avatar_b64 = base64.b64encode(av_resp.content).decode('utf-8')
            except:
                pass
            
            avatar_svg = ''
            if avatar_b64:
                avatar_svg = f'<image href="data:image/png;base64,{avatar_b64}" x="16" y="16" width="72" height="72" rx="8" clip-path="url(#avatarClip)"/>'
            else:
                # Fallback: first letter
                avatar_svg = f'<rect x="16" y="16" width="72" height="72" rx="8" fill="{t["bg2"]}" stroke="{t["border"]}" stroke-width="1.5"/><text x="52" y="62" font-size="36" font-weight="700" fill="{t["title"]}" text-anchor="middle">{esc(display_name[0].upper())}</text>'
            
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="220" viewBox="0 0 440 220" font-family="'Segoe UI', '-apple-system', Arial, sans-serif">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{t["bg"]}"/>
      <stop offset="100%" style="stop-color:{t["bg2"]}"/>
    </linearGradient>
    <linearGradient id="bar1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{t["accent"]}"/>
      <stop offset="100%" style="stop-color:{t["accent2"]}"/>
    </linearGradient>
    <linearGradient id="bar2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{t["accent2"]}"/>
      <stop offset="100%" style="stop-color:{t["border"]}"/>
    </linearGradient>
    <linearGradient id="bar3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{t["gold"]}"/>
      <stop offset="100%" style="stop-color:{t["accent"]}"/>
    </linearGradient>
    <linearGradient id="bar4" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{t["border"]}"/>
      <stop offset="100%" style="stop-color:{t["title"]}"/>
    </linearGradient>
    <linearGradient id="topBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{t["accent"]}"/>
      <stop offset="50%" style="stop-color:{t["border"]}"/>
      <stop offset="100%" style="stop-color:{t["accent2"]}"/>
    </linearGradient>
    <clipPath id="avatarClip">
      <rect x="16" y="16" width="72" height="72" rx="8"/>
    </clipPath>
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <!-- Card background -->
  <rect width="440" height="220" rx="12" fill="url(#bgGrad)" stroke="{t["border"]}" stroke-width="1"/>
  
  <!-- Top accent bar -->
  <rect width="440" height="3" rx="12" fill="url(#topBar)"/>
  
  <!-- Avatar -->
  {avatar_svg}
  
  <!-- Name & username -->
  <text x="100" y="40" font-size="18" font-weight="700" fill="{t["title"]}">{esc(display_name)}</text>
  <text x="100" y="58" font-size="12" fill="{t["subtext"]}">@{esc(username)}</text>
  <text x="100" y="76" font-size="10" fill="{t["text"]}">Since {created_at}</text>
  
  <!-- Divider -->
  <line x1="16" y1="100" x2="424" y2="100" stroke="{t["border"]}" stroke-width="0.5" opacity="0.3"/>
  
  <!-- Stats with bars -->
  <!-- Repositories -->
  <g transform="translate(16, 115)">
    <circle cx="6" cy="-2" r="4" fill="{t["accent"]}"/>
    <text x="18" y="2" font-size="11" fill="{t["subtext"]}">Repositories</text>
    <text x="408" y="2" font-size="14" font-weight="700" fill="{t["text"]}" text-anchor="end">{repos_count}</text>
    <rect x="0" y="8" width="408" height="5" rx="2.5" fill="{t["bg"]}" opacity="0.6"/>
    <rect x="0" y="8" width="{bar_width(repos_count, 30):.0f}" height="5" rx="2.5" fill="url(#bar1)"/>
  </g>
  
  <!-- Followers -->
  <g transform="translate(16, 140)">
    <circle cx="6" cy="-2" r="4" fill="{t["accent2"]}"/>
    <text x="18" y="2" font-size="11" fill="{t["subtext"]}">Followers</text>
    <text x="408" y="2" font-size="14" font-weight="700" fill="{t["text"]}" text-anchor="end">{followers}</text>
    <rect x="0" y="8" width="408" height="5" rx="2.5" fill="{t["bg"]}" opacity="0.6"/>
    <rect x="0" y="8" width="{bar_width(followers, 50):.0f}" height="5" rx="2.5" fill="url(#bar2)"/>
  </g>
  
  <!-- Stars -->
  <g transform="translate(16, 165)">
    <circle cx="6" cy="-2" r="4" fill="{t["gold"]}"/>
    <text x="18" y="2" font-size="11" fill="{t["subtext"]}">Total Stars</text>
    <text x="408" y="2" font-size="14" font-weight="700" fill="{t["gold"]}" text-anchor="end">&#9733; {stars_total}</text>
    <rect x="0" y="8" width="408" height="5" rx="2.5" fill="{t["bg"]}" opacity="0.6"/>
    <rect x="0" y="8" width="{bar_width(stars_total, 50):.0f}" height="5" rx="2.5" fill="url(#bar3)"/>
  </g>
  
  <!-- Forks -->
  <g transform="translate(16, 190)">
    <circle cx="6" cy="-2" r="4" fill="{t["border"]}"/>
    <text x="18" y="2" font-size="11" fill="{t["subtext"]}">Forks</text>
    <text x="408" y="2" font-size="14" font-weight="700" fill="{t["text"]}" text-anchor="end">{forks_total}</text>
    <rect x="0" y="8" width="408" height="5" rx="2.5" fill="{t["bg"]}" opacity="0.6"/>
    <rect x="0" y="8" width="{bar_width(forks_total, 20):.0f}" height="5" rx="2.5" fill="url(#bar4)"/>
  </g>
  
</svg>'''
            
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(svg.encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())
