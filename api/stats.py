import os
import json
import requests
from datetime import datetime
from urllib.parse import quote

def generate_svg(username, stats):
    """Generate GitHub stats SVG card with Rikka Takanashi anime theme"""
    
    # Rikka color scheme (purple/teal/dark)
    bg_color = "#0f1419"
    primary_color = "#7c3aed"  # Rikka purple
    accent_color = "#14b8a6"   # Teal accent
    text_color = "#e5e7eb"     # Light gray
    stat_color = "#38bdae"     # Bright teal
    
    repos = stats.get('public_repos', 0)
    followers = stats.get('followers', 0)
    following = stats.get('following', 0)
    created_at = stats.get('created_at', '').split('T')[0]
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="200" viewBox="0 0 500 200">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&display=swap');
      text {{ font-family: 'Fira Code', monospace; }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="500" height="200" rx="8" fill="{bg_color}" stroke="{primary_color}" stroke-width="2"/>
  
  <!-- Accent border top -->
  <line x1="0" y1="8" x2="500" y2="8" stroke="{primary_color}" stroke-width="2"/>
  
  <!-- Header -->
  <text x="20" y="35" font-size="24" font-weight="600" fill="{primary_color}">@{username}</text>
  <text x="20" y="55" font-size="12" fill="{text_color}">GitHub Stats Card</text>
  
  <!-- Stats Grid -->
  <!-- Repos -->
  <g>
    <circle cx="80" cy="110" r="8" fill="{accent_color}"/>
    <text x="95" y="115" font-size="14" font-weight="600" fill="{stat_color}">{repos}</text>
    <text x="95" y="130" font-size="11" fill="{text_color}">Repositories</text>
  </g>
  
  <!-- Followers -->
  <g>
    <circle cx="230" cy="110" r="8" fill="{accent_color}"/>
    <text x="245" y="115" font-size="14" font-weight="600" fill="{stat_color}">{followers}</text>
    <text x="245" y="130" font-size="11" fill="{text_color}">Followers</text>
  </g>
  
  <!-- Following -->
  <g>
    <circle cx="380" cy="110" r="8" fill="{accent_color}"/>
    <text x="395" y="115" font-size="14" font-weight="600" fill="{stat_color}">{following}</text>
    <text x="395" y="130" font-size="11" fill="{text_color}">Following</text>
  </g>
  
  <!-- Joined -->
  <text x="20" y="170" font-size="11" fill="{text_color}">Joined: {created_at}</text>
  
  <!-- Rikka signature -->
  <text x="450" y="170" font-size="10" fill="{primary_color}" text-anchor="end">Rikka</text>
  
  <!-- Decorative corner -->
  <polygon points="500,0 500,15 485,0" fill="{primary_color}"/>
</svg>'''
    
    return svg

def handler(request):
    """Vercel serverless handler"""
    try:
        # Get username from query params
        username = request.args.get('username', 'rikka0x')
        theme = request.args.get('theme', 'rikka')
        
        if not username:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'username parameter required'})
            }
        
        # Fetch from GitHub API
        github_api = f'https://api.github.com/users/{username}'
        response = requests.get(github_api, timeout=10)
        
        if response.status_code != 200:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'User {username} not found'})
            }
        
        stats = response.json()
        svg = generate_svg(username, stats)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': 'public, max-age=3600'
            },
            'body': svg
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
