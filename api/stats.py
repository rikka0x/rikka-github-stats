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
            
            # Fetch GitHub stats
            response = requests.get(
                f'https://api.github.com/users/{username}',
                timeout=10,
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            if response.status_code != 200:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'User not found')
                return
            
            stats = response.json()
            
            # Fetch contribution data
            repos_count = stats.get('public_repos', 0)
            followers = stats.get('followers', 0)
            following = stats.get('following', 0)
            created_at = stats.get('created_at', '').split('T')[0]
            display_name = stats.get('name', username) or username
            
            # Fetch repo stars and forks
            stars_total = 0
            forks_total = 0
            try:
                repos_response = requests.get(
                    f'https://api.github.com/users/{username}/repos?per_page=100',
                    timeout=10,
                    headers={'Accept': 'application/vnd.github.v3+json'}
                )
                if repos_response.status_code == 200:
                    for repo in repos_response.json():
                        stars_total += repo.get('stargazers_count', 0)
                        forks_total += repo.get('forks_count', 0)
            except:
                pass
            
            # Escape XML
            def esc(s):
                return s.replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"')
            
            # Color palette — Rikka Takanashi theme
            bg_dark = '#0d0b1a'
            bg_card = '#1a1530'
            purple = '#7c3aed'
            purple_light = '#a78bfa'
            teal = '#14b8a6'
            teal_light = '#2dd4bf'
            pink = '#ec4899'
            text_main = '#e2e8f0'
            text_dim = '#94a3b8'
            gold = '#fbbf24'
            
            # Calculate progress bar widths (max 160px)
            repos_pct = min(repos_count / 20 * 160, 160)
            followers_pct = min(followers / 50 * 160, 160)
            stars_pct = min(stars_total / 50 * 160, 160)
            
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_dark};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{bg_card};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{purple};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{purple_light};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{teal};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{teal_light};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="pinkGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{pink};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{purple};stop-opacity:1" />
    </linearGradient>
    <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:{teal};stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:{teal};stop-opacity:0" />
    </radialGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="495" height="195" rx="12" fill="url(#bgGrad)" stroke="{purple}" stroke-width="1.5" opacity="0.95"/>
  
  <!-- Top gradient bar -->
  <rect width="495" height="4" rx="12" fill="url(#purpleGrad)"/>
  
  <!-- Magic circle decoration (top-right) -->
  <g transform="translate(440, 25)" opacity="0.15">
    <circle cx="0" cy="0" r="22" fill="none" stroke="{purple_light}" stroke-width="1"/>
    <circle cx="0" cy="0" r="16" fill="none" stroke="{teal}" stroke-width="0.8"/>
    <circle cx="0" cy="0" r="10" fill="none" stroke="{purple_light}" stroke-width="0.5"/>
    <line x1="-22" y1="0" x2="22" y2="0" stroke="{purple_light}" stroke-width="0.5"/>
    <line x1="0" y1="-22" x2="0" y2="22" stroke="{purple_light}" stroke-width="0.5"/>
    <line x1="-16" y1="-16" x2="16" y2="16" stroke="{teal}" stroke-width="0.5"/>
    <line x1="-16" y1="16" x2="16" y2="-16" stroke="{teal}" stroke-width="0.5"/>
  </g>
  
  <!-- Rikka character silhouette (left side) -->
  <g transform="translate(8, 12)">
    <!-- Hair backlight (purple glow) -->
    <ellipse cx="42" cy="35" rx="32" ry="38" fill="{purple}" opacity="0.2" filter="url(#glow)"/>
    
    <!-- Hair back layer (long, flowing) -->
    <path d="M 15,50 Q 8,25 18,15 Q 25,8 35,10 Q 42,5 50,8 Q 58,5 65,12 Q 75,18 72,35 Q 75,55 70,80 Q 68,95 65,105 Q 60,115 55,118 L 25,118 Q 20,115 18,105 Q 15,90 12,75 Q 10,60 15,50 Z" fill="#1e1b3a" stroke="{purple}" stroke-width="0.8"/>
    
    <!-- Hair front bangs (Rikka's signature) -->
    <path d="M 20,20 Q 22,12 30,10 Q 35,8 40,12 Q 42,8 48,10 Q 52,8 58,12 Q 65,10 70,18 Q 72,25 68,32 Q 65,28 62,30 Q 58,26 55,30 Q 52,26 48,30 Q 45,26 42,30 Q 38,26 35,30 Q 32,26 28,30 Q 25,28 22,32 Q 18,28 20,20 Z" fill="#2a1f4a" stroke="{purple_light}" stroke-width="0.5"/>
    
    <!-- Face -->
    <ellipse cx="45" cy="40" rx="16" ry="18" fill="#f5e6d3" opacity="0.95"/>
    
    <!-- Eye patch (Rikka's signature right eye) -->
    <g transform="translate(52, 35)">
      <rect x="-5" y="-3" width="12" height="7" rx="2" fill="{bg_dark}" stroke="{teal}" stroke-width="0.8"/>
      <line x1="-7" y1="0" x2="7" y2="0" stroke="{teal}" stroke-width="1.5" filter="url(#glow)"/>
      <circle cx="0" cy="0" r="5" fill="url(#eyeGlow)"/>
    </g>
    
    <!-- Left eye ( visible, teal-colored) -->
    <g transform="translate(38, 38)">
      <ellipse cx="0" cy="0" rx="3.5" ry="4.5" fill="white" stroke="{purple}" stroke-width="0.5"/>
      <circle cx="0" cy="0" r="2.5" fill="{teal}" filter="url(#glow)"/>
      <circle cx="0" cy="-0.5" r="1" fill="white"/>
    </g>
    
    <!-- Small smile -->
    <path d="M 40,50 Q 45,53 50,50" fill="none" stroke="#c08484" stroke-width="1" stroke-linecap="round"/>
    
    <!-- Hair strand accents (yellow ribbon tie) -->
    <g transform="translate(25, 18)">
      <path d="M 0,0 L -5,-4 L -3,2 L -7,4 L 2,3 Z" fill="{gold}" opacity="0.9"/>
    </g>
    <g transform="translate(68, 20)">
      <path d="M 0,0 L 5,-4 L 3,2 L 7,4 L -2,3 Z" fill="{gold}" opacity="0.9"/>
    </g>
    
    <!-- Magical sparkles around character -->
    <g opacity="0.6">
      <text x="5" y="15" font-size="8" fill="{teal}">&#10022;</text>
      <text x="75" y="50" font-size="6" fill="{purple_light}">&#10022;</text>
      <text x="3" y="70" font-size="5" fill="{pink}">&#10022;</text>
      <text x="72" y="85" font-size="7" fill="{teal}">&#10022;</text>
    </g>
  </g>
  
  <!-- Divider line -->
  <line x1="100" y1="15" x2="100" y2="180" stroke="{purple}" stroke-width="0.5" opacity="0.3"/>
  
  <!-- Header text -->
  <text x="115" y="30" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="700" fill="{purple_light}" filter="url(#glow)">&#9881; GitHub Stats</text>
  <text x="115" y="47" font-family="'Fira Code', monospace" font-size="12" font-weight="600" fill="{text_main}">{esc(display_name)}</text>
  <text x="115" y="62" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">@{esc(username)}</text>
  
  <!-- Stats with progress bars -->
  <!-- Repositories -->
  <g transform="translate(115, 75)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">Repositories</text>
    <text x="160" y="0" font-family="'Fira Code', monospace" font-size="12" font-weight="700" fill="{teal_light}" text-anchor="end">{repos_count}</text>
    <rect x="0" y="5" width="160" height="4" rx="2" fill="{bg_dark}" stroke="{purple}" stroke-width="0.3" opacity="0.5"/>
    <rect x="0" y="5" width="{repos_pct:.0f}" height="4" rx="2" fill="url(#tealGrad)"/>
  </g>
  
  <!-- Followers -->
  <g transform="translate(290, 75)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">Followers</text>
    <text x="170" y="0" font-family="'Fira Code', monospace" font-size="12" font-weight="700" fill="{purple_light}" text-anchor="end">{followers}</text>
    <rect x="0" y="5" width="170" height="4" rx="2" fill="{bg_dark}" stroke="{purple}" stroke-width="0.3" opacity="0.5"/>
    <rect x="0" y="5" width="{followers_pct:.0f}" height="4" rx="2" fill="url(#purpleGrad)"/>
  </g>
  
  <!-- Stars -->
  <g transform="translate(115, 100)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">Total Stars</text>
    <text x="160" y="0" font-family="'Fira Code', monospace" font-size="12" font-weight="700" fill="{gold}" text-anchor="end">&#9733; {stars_total}</text>
    <rect x="0" y="5" width="160" height="4" rx="2" fill="{bg_dark}" stroke="{purple}" stroke-width="0.3" opacity="0.5"/>
    <rect x="0" y="5" width="{stars_pct:.0f}" height="4" rx="2" fill="{gold}" opacity="0.8"/>
  </g>
  
  <!-- Following -->
  <g transform="translate(290, 100)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">Following</text>
    <text x="170" y="0" font-family="'Fira Code', monospace" font-size="12" font-weight="700" fill="{pink}" text-anchor="end">{following}</text>
    <rect x="0" y="5" width="170" height="4" rx="2" fill="{bg_dark}" stroke="{purple}" stroke-width="0.3" opacity="0.5"/>
    <rect x="0" y="5" width="{min(following / 30 * 170, 170):.0f}" height="4" rx="2" fill="url(#pinkGrad)"/>
  </g>
  
  <!-- Forks -->
  <g transform="translate(115, 125)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">Forks</text>
    <text x="160" y="0" font-family="'Fira Code', monospace" font-size="12" font-weight="700" fill="{teal_light}" text-anchor="end">{forks_total}</text>
    <rect x="0" y="5" width="160" height="4" rx="2" fill="{bg_dark}" stroke="{purple}" stroke-width="0.3" opacity="0.5"/>
    <rect x="0" y="5" width="{min(forks_total / 20 * 160, 160):.0f}" height="4" rx="2" fill="url(#tealGrad)"/>
  </g>
  
  <!-- Joined date -->
  <g transform="translate(290, 125)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="{text_dim}">Joined</text>
    <text x="170" y="0" font-family="'Fira Code', monospace" font-size="12" font-weight="600" fill="{text_main}" text-anchor="end">{created_at}</text>
  </g>
  
  <!-- Bottom decoration: magic circle + text -->
  <g transform="translate(135, 165)" opacity="0.7">
    <circle cx="0" cy="0" r="6" fill="none" stroke="{purple_light}" stroke-width="0.5"/>
    <circle cx="0" cy="0" r="3" fill="none" stroke="{teal}" stroke-width="0.3"/>
    <text x="12" y="4" font-family="'Fira Code', monospace" font-size="9" fill="{purple_light}" font-style="italic">&#10024; Wielder of the Tyrant's Eye &#10024;</text>
  </g>
  
  <!-- Corner accents -->
  <polygon points="480,195 495,195 495,180" fill="{purple}" opacity="0.5"/>
  <polygon points="0,195 0,180 15,195" fill="{teal}" opacity="0.3"/>
  
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
