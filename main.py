"""
Daily Social Indexing & Pinterest/Facebook Image Pin Automation
Main entry point - dispatches to appropriate action based on PUZZLE_TYPE env var
"""

import os
import sys
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from indexing import submit_urls_for_indexing
from image_generator import generate_pinterest_image, generate_facebook_image
from pinterest_poster import upload_image_to_pinterest
from facebook_poster import post_image_to_facebook

# Puzzle configurations with their Pinterest Board IDs
PUZZLES = {
    "wordle": {
        "name": "Wordle",
        "board_id": "924434329702687588",
        "color": "#6aaa64",  # Green
        "gradient": ["#6aaa64", "#538d4e"]
    },
    "quordle": {
        "name": "Quordle",
        "board_id": "924434329702687592",
        "color": "#9b59b6",  # Purple
        "gradient": ["#9b59b6", "#8e44ad"]
    },
    "colordle": {
        "name": "Colordle",
        "board_id": "924434329702687590",
        "color": "#e74c3c",  # Red
        "gradient": ["#e74c3c", "#c0392b"]
    },
    "semantle": {
        "name": "Semantle",
        "board_id": "924434329702687594",
        "color": "#3498db",  # Blue
        "gradient": ["#3498db", "#2980b9"]
    },
    "phoodle": {
        "name": "Phoodle",
        "board_id": "924434329702687593",
        "color": "#f39c12",  # Orange
        "gradient": ["#f39c12", "#e67e22"]
    }
}

BASE_URL = "https://wordsolverx.com"

def get_ist_now():
    """Get current time in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def format_date_for_url(date_obj):
    """Format date as month-day-year for URL (e.g., january-17-2026)"""
    return date_obj.strftime('%B-%d-%Y').lower()

def format_date_for_display(date_obj):
    """Format date for display (e.g., January 17, 2026)"""
    return date_obj.strftime('%B %d, %Y')

def generate_dynamic_urls(ist_now):
    """Generate all URLs for indexing (today ±2 days × 5 puzzles)"""
    urls = []
    
    # Generate dates: today, +1, +2, -1, -2
    for day_offset in [-2, -1, 0, 1, 2]:
        date = ist_now + timedelta(days=day_offset)
        date_str = format_date_for_url(date)
        
        for puzzle_key in PUZZLES.keys():
            url = f"{BASE_URL}/{puzzle_key}-answer-for-{date_str}"
            urls.append(url)
    
    return urls

def load_pages_txt():
    """Load additional URLs from pages.txt if it exists"""
    pages_file = os.path.join(os.path.dirname(__file__), 'pages.txt')
    urls = []
    
    if os.path.exists(pages_file):
        with open(pages_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        print(f"Loaded {len(urls)} URLs from pages.txt")
    
    return urls

def run_indexing():
    """Submit all URLs for Google Indexing"""
    print("\n=== Starting Google Indexing ===")
    ist_now = get_ist_now()
    
    # Get dynamic URLs
    dynamic_urls = generate_dynamic_urls(ist_now)
    print(f"Generated {len(dynamic_urls)} dynamic URLs")
    
    # Get static URLs from pages.txt
    static_urls = load_pages_txt()
    
    # Combine all URLs
    all_urls = dynamic_urls + static_urls
    print(f"Total URLs to index: {len(all_urls)}")
    
    # Submit for indexing
    submit_urls_for_indexing(all_urls)

def run_social_post(puzzle_key):
    """Create and post image pin for a specific puzzle"""
    if puzzle_key not in PUZZLES:
        print(f"Unknown puzzle type: {puzzle_key}")
        return
    
    puzzle = PUZZLES[puzzle_key]
    ist_now = get_ist_now()
    
    print(f"\n=== Creating {puzzle['name']} Pin ===")
    
    # Generate date info
    date_display = format_date_for_display(ist_now)
    title = f"{puzzle['name']} Answer for {date_display}"
    
    # Generate URL for the pin link
    date_url = format_date_for_url(ist_now)
    permalink = f"{BASE_URL}/{puzzle_key}-answer-for-{date_url}"
    
    # Generate Pinterest image (1000x1500 - portrait)
    print("Generating Pinterest image (1000x1500)...")
    pinterest_image = generate_pinterest_image(
        puzzle_name=puzzle['name'],
        date_str=date_display,
        theme_colors=puzzle['gradient']
    )
    
    if not pinterest_image:
        print(f"Failed to generate Pinterest image for {puzzle['name']}")
    else:
        # Upload to Pinterest
        print(f"Uploading to Pinterest (Board: {puzzle['board_id']})...")
        upload_image_to_pinterest(
            image_path=pinterest_image,
            title=title,
            description=f"Find today's {puzzle['name']} answer and hints! Visit {permalink}",
            link=permalink,
            board_id=puzzle['board_id']
        )
        # Cleanup Pinterest image
        if os.path.exists(pinterest_image):
            os.remove(pinterest_image)
            print(f"Cleaned up Pinterest image")
    
    # Generate Facebook image (1200x628 - landscape)
    print("Generating Facebook image (1200x628)...")
    facebook_image = generate_facebook_image(
        puzzle_name=puzzle['name'],
        date_str=date_display,
        theme_colors=puzzle['gradient']
    )
    
    if not facebook_image:
        print(f"Failed to generate Facebook image for {puzzle['name']}")
    else:
        # Post to Facebook
        print("Posting to Facebook...")
        post_image_to_facebook(
            image_path=facebook_image,
            caption=f"🎯 {title}\n\n🔗 {permalink}\n\n#Wordle #{puzzle['name']} #WordGames #PuzzleGames"
        )
        # Cleanup Facebook image
        if os.path.exists(facebook_image):
            os.remove(facebook_image)
            print(f"Cleaned up Facebook image")

def main():
    """Main entry point"""
    action = os.environ.get('ACTION', 'indexing')
    puzzle_type = os.environ.get('PUZZLE_TYPE', '').lower()
    
    print(f"Action: {action}")
    print(f"Puzzle Type: {puzzle_type or 'N/A'}")
    print(f"Current IST: {get_ist_now()}")
    
    if action == 'indexing':
        run_indexing()
    elif action == 'social':
        if puzzle_type:
            run_social_post(puzzle_type)
        else:
            print("PUZZLE_TYPE not specified for social action")
            sys.exit(1)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
