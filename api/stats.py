import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query params
            query_path = self.path.split('?')[1] if '?' in self.path else ''
            params = {}
            for param in query_path.split('&'):
                if '=' in param:
                    key, val = param.split('=', 1)
                    params[key] = val
            
            username = params.get('username', 'rikka0x')
            
            # Fetch GitHub stats
            response = requests.get(f'https://api.github.com/users/{username}', timeout=10)
            
            if response.status_code != 200:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'User not found')
                return
            
            stats = response.json()
            
            # Generate SVG
            repos = stats.get('public_repos', 0)
            followers = stats.get('followers', 0)
            following = stats.get('following', 0)
            created_at = stats.get('created_at', '').split('T')[0]
            
            display_name = stats.get('name', username)
            if display_name and display_name != username:
                display_name = display_name.replace('&', '&')
            else:
                display_name = f'@{username}'
            
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="200" viewBox="0 0 500 200">
  <defs>
    <style>
      text {{ font-family: 'Fira Code', monospace; }}
    </style>
  </defs>
  <rect width="500" height="200" rx="8" fill="#0f1419" stroke="#7c3aed" stroke-width="2"/>
  <line x1="0" y1="8" x2="500" y2="8" stroke="#7c3aed" stroke-width="2"/>
  <text x="20" y="35" font-size="24" font-weight="600" fill="#7c3aed">{display_name}</text>
  <text x="20" y="55" font-size="12" fill="#e5e7eb">GitHub Stats</text>
  <g>
    <circle cx="80" cy="110" r="8" fill="#14b8a6"/>
    <text x="95" y="115" font-size="14" font-weight="600" fill="#38bdae">{repos}</text>
    <text x="95" y="130" font-size="11" fill="#e5e7eb">Repositories</text>
  </g>
  <g>
    <circle cx="230" cy="110" r="8" fill="#14b8a6"/>
    <text x="245" y="115" font-size="14" font-weight="600" fill="#38bdae">{followers}</text>
    <text x="245" y="130" font-size="11" fill="#e5e7eb">Followers</text>
  </g>
  <g>
    <circle cx="380" cy="110" r="8" fill="#14b8a6"/>
    <text x="395" y="115" font-size="14" font-weight="600" fill="#38bdae">{following}</text>
    <text x="395" y="130" font-size="11" fill="#e5e7eb">Following</text>
  </g>
  <text x="20" y="170" font-size="11" fill="#e5e7eb">Joined: {created_at}</text>
  <text x="450" y="170" font-size="10" fill="#7c3aed" text-anchor="end">Rikka</text>
  <polygon points="500,0 500,15 485,0" fill="#7c3aed"/>
</svg>'''
            
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.end_headers()
            self.wfile.write(svg.encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())
