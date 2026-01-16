"""
Professional Image Generator for Social Media
Creates attractive, readable images for Pinterest and Facebook
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import tempfile
import urllib.request

# Font URLs for downloading professional fonts
FONT_URLS = {
    "bold": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
    "semibold": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-SemiBold.ttf",
    "regular": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",
}

FONT_CACHE = {}

def get_font(style, size):
    """Get a font, downloading if necessary"""
    cache_key = f"{style}_{size}"
    if cache_key in FONT_CACHE:
        return FONT_CACHE[cache_key]
    
    font_dir = os.path.join(tempfile.gettempdir(), "social_fonts")
    os.makedirs(font_dir, exist_ok=True)
    
    font_path = os.path.join(font_dir, f"Poppins-{style.capitalize()}.ttf")
    
    if not os.path.exists(font_path):
        try:
            url = FONT_URLS.get(style, FONT_URLS["regular"])
            print(f"Downloading font: {style}...")
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            print(f"Failed to download font: {e}")
            # Fallback to system fonts
            try:
                font = ImageFont.truetype("arial.ttf", size)
                FONT_CACHE[cache_key] = font
                return font
            except:
                font = ImageFont.load_default()
                FONT_CACHE[cache_key] = font
                return font
    
    try:
        font = ImageFont.truetype(font_path, size)
        FONT_CACHE[cache_key] = font
        return font
    except:
        font = ImageFont.load_default()
        FONT_CACHE[cache_key] = font
        return font


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_gradient(width, height, start_color, end_color, direction="vertical"):
    """Create a gradient image"""
    img = Image.new('RGB', (width, height))
    
    for y in range(height):
        ratio = y / height if direction == "vertical" else 0
        for x in range(width):
            if direction == "horizontal":
                ratio = x / width
            elif direction == "diagonal":
                ratio = (x + y) / (width + height)
            
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            img.putpixel((x, y), (r, g, b))
    
    return img


def draw_text_with_outline(draw, text, position, font, fill_color, outline_color, outline_width=3):
    """Draw text with outline for better visibility"""
    x, y = position
    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    # Draw main text
    draw.text(position, text, font=font, fill=fill_color)


def get_text_dimensions(draw, text, font):
    """Get text width and height"""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered_text(draw, text, y, width, font, color, outline=False, outline_color=(0, 0, 0)):
    """Draw horizontally centered text"""
    text_width, text_height = get_text_dimensions(draw, text, font)
    x = (width - text_width) // 2
    
    if outline:
        draw_text_with_outline(draw, text, (x, y), font, color, outline_color, outline_width=4)
    else:
        draw.text((x, y), text, font=font, fill=color)
    
    return text_height


def draw_puzzle_icon_large(draw, center_x, center_y, puzzle_name, box_size=80, gap=12):
    """Draw a large, prominent puzzle icon"""
    puzzle = puzzle_name.lower()
    
    if puzzle == "wordle":
        # 5 boxes in a row - Wordle style
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        colors = ["#6aaa64", "#c9b458", "#6aaa64", "#6aaa64", "#c9b458"]
        letters = ["W", "O", "R", "D", "S"]
        
        for i, (color, letter) in enumerate(zip(colors, letters)):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, center_y - box_size//2, x + box_size, center_y + box_size//2], 
                                   radius=12, fill=color)
            # Draw letter
            letter_font = get_font("bold", int(box_size * 0.6))
            lw, lh = get_text_dimensions(draw, letter, letter_font)
            draw.text((x + (box_size - lw)//2, center_y - lh//2 - 5), letter, 
                     font=letter_font, fill="white")
    
    elif puzzle == "quordle":
        # 2x2 grid - Quordle style
        total_size = 2 * box_size + gap
        start_x = center_x - total_size // 2
        start_y = center_y - total_size // 2
        colors = ["#6aaa64", "#c9b458", "#787c7e", "#6aaa64"]
        letters = ["Q", "U", "A", "D"]
        
        for i in range(4):
            row, col = i // 2, i % 2
            x = start_x + col * (box_size + gap)
            y = start_y + row * (box_size + gap)
            draw.rounded_rectangle([x, y, x + box_size, y + box_size], 
                                   radius=12, fill=colors[i])
            letter_font = get_font("bold", int(box_size * 0.5))
            lw, lh = get_text_dimensions(draw, letters[i], letter_font)
            draw.text((x + (box_size - lw)//2, y + (box_size - lh)//2 - 3), letters[i], 
                     font=letter_font, fill="white")
    
    elif puzzle == "colordle":
        # Rainbow color boxes
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        colors = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#3498db"]
        
        for i, color in enumerate(colors):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, center_y - box_size//2, x + box_size, center_y + box_size//2], 
                                   radius=12, fill=color, outline="white", width=3)
    
    elif puzzle == "semantle":
        # Gradient similarity boxes
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        
        for i in range(5):
            x = start_x + i * (box_size + gap)
            # Blue gradient from light to dark
            blue_intensity = int(100 + (155 * (i + 1) / 5))
            color = f"#3498db" if i == 4 else f"#{50+i*30:02x}{100+i*30:02x}{200+i*10:02x}"
            draw.rounded_rectangle([x, center_y - box_size//2, x + box_size, center_y + box_size//2], 
                                   radius=12, fill=color)
            # Percentage text
            pct = f"{20 + i * 20}%"
            pct_font = get_font("bold", int(box_size * 0.35))
            pw, ph = get_text_dimensions(draw, pct, pct_font)
            draw.text((x + (box_size - pw)//2, center_y - ph//2), pct, 
                     font=pct_font, fill="white")
    
    elif puzzle == "phoodle":
        # Food-themed colorful boxes
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        colors = ["#e67e22", "#27ae60", "#e74c3c", "#f39c12", "#2ecc71"]
        letters = ["F", "O", "O", "D", "S"]
        
        for i, (color, letter) in enumerate(zip(colors, letters)):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, center_y - box_size//2, x + box_size, center_y + box_size//2], 
                                   radius=12, fill=color)
            letter_font = get_font("bold", int(box_size * 0.6))
            lw, lh = get_text_dimensions(draw, letter, letter_font)
            draw.text((x + (box_size - lw)//2, center_y - lh//2 - 5), letter, 
                     font=letter_font, fill="white")


def generate_pinterest_image(puzzle_name, date_str, theme_colors=None):
    """
    Generate a professional Pinterest pin image.
    Pinterest optimal size: 1000x1500 (2:3 ratio)
    """
    width, height = 1000, 1500
    
    # Theme colors for different puzzles
    themes = {
        "wordle": {"gradient": ["#538d4e", "#3a5f3a"], "accent": "#6aaa64"},
        "quordle": {"gradient": ["#9b59b6", "#6c3483"], "accent": "#a855f7"},
        "colordle": {"gradient": ["#e74c3c", "#922b21"], "accent": "#e74c3c"},
        "semantle": {"gradient": ["#3498db", "#1a5276"], "accent": "#3498db"},
        "phoodle": {"gradient": ["#e67e22", "#a04000"], "accent": "#f39c12"},
    }
    
    theme = themes.get(puzzle_name.lower(), themes["wordle"])
    if theme_colors:
        theme["gradient"] = theme_colors
    
    # Create gradient background
    start_color = hex_to_rgb(theme["gradient"][0])
    end_color = hex_to_rgb(theme["gradient"][1])
    img = create_gradient(width, height, start_color, end_color)
    draw = ImageDraw.Draw(img)
    
    # Add subtle pattern (dots)
    for x in range(0, width, 60):
        for y in range(0, height, 60):
            draw.ellipse([x-4, y-4, x+4, y+4], fill=(255, 255, 255, 40))
    
    # Add decorative corners
    corner_size = 200
    draw.polygon([(0, 0), (corner_size, 0), (0, corner_size)], 
                 fill=(*hex_to_rgb(theme["accent"]), 100))
    draw.polygon([(width, height), (width - corner_size, height), (width, height - corner_size)], 
                 fill=(*hex_to_rgb(theme["accent"]), 100))
    
    # === CONTENT ===
    
    # Draw puzzle icon at top
    icon_y = 350
    draw_puzzle_icon_large(draw, width // 2, icon_y, puzzle_name, box_size=100, gap=15)
    
    # Main title: "{Puzzle} Answer"
    title_font = get_font("bold", 90)
    title_text = f"{puzzle_name} Answer"
    draw_centered_text(draw, title_text, 550, width, title_font, "white", outline=True)
    
    # Subtitle: "for"
    subtitle_font = get_font("regular", 50)
    draw_centered_text(draw, "for", 680, width, subtitle_font, (220, 220, 220))
    
    # Date - LARGE and prominent
    date_font = get_font("semibold", 75)
    draw_centered_text(draw, date_str, 760, width, date_font, "white", outline=True)
    
    # Decorative line
    line_y = 900
    line_width = 400
    draw.line([(width//2 - line_width//2, line_y), (width//2 + line_width//2, line_y)], 
              fill=(255, 255, 255, 150), width=3)
    
    # Call to action
    cta_font = get_font("semibold", 45)
    draw_centered_text(draw, "Get Today's Hints & Answer", 980, width, cta_font, (255, 255, 200))
    
    # Website branding at bottom
    brand_font = get_font("bold", 55)
    draw_centered_text(draw, "wordsolverx.com", 1350, width, brand_font, "white", outline=True)
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='_pinterest.png', delete=False)
    img.save(temp_file.name, 'PNG', quality=95)
    print(f"Generated Pinterest image: {temp_file.name}")
    
    return temp_file.name


def generate_facebook_image(puzzle_name, date_str, theme_colors=None):
    """
    Generate a professional Facebook post image.
    Facebook optimal size: 1200x628 (1.91:1 ratio)
    """
    width, height = 1200, 628
    
    # Theme colors for different puzzles
    themes = {
        "wordle": {"gradient": ["#538d4e", "#3a5f3a"], "accent": "#6aaa64"},
        "quordle": {"gradient": ["#9b59b6", "#6c3483"], "accent": "#a855f7"},
        "colordle": {"gradient": ["#e74c3c", "#922b21"], "accent": "#e74c3c"},
        "semantle": {"gradient": ["#3498db", "#1a5276"], "accent": "#3498db"},
        "phoodle": {"gradient": ["#e67e22", "#a04000"], "accent": "#f39c12"},
    }
    
    theme = themes.get(puzzle_name.lower(), themes["wordle"])
    if theme_colors:
        theme["gradient"] = theme_colors
    
    # Create gradient background (horizontal for Facebook)
    start_color = hex_to_rgb(theme["gradient"][0])
    end_color = hex_to_rgb(theme["gradient"][1])
    img = create_gradient(width, height, start_color, end_color, direction="horizontal")
    draw = ImageDraw.Draw(img)
    
    # Add subtle pattern
    for x in range(0, width, 50):
        for y in range(0, height, 50):
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 255, 30))
    
    # Left section: Puzzle icon
    icon_x = 250
    icon_y = height // 2
    draw_puzzle_icon_large(draw, icon_x, icon_y, puzzle_name, box_size=70, gap=10)
    
    # Right section: Text content
    text_x_center = 750
    
    # Title
    title_font = get_font("bold", 70)
    title_text = f"{puzzle_name} Answer"
    title_width, _ = get_text_dimensions(draw, title_text, title_font)
    draw_text_with_outline(draw, title_text, (text_x_center - title_width//2, 120), 
                          title_font, "white", (0, 0, 0), 3)
    
    # Date - prominent
    date_font = get_font("semibold", 55)
    date_width, _ = get_text_dimensions(draw, date_str, date_font)
    draw_text_with_outline(draw, date_str, (text_x_center - date_width//2, 230), 
                          date_font, "white", (0, 0, 0), 2)
    
    # Call to action
    cta_font = get_font("regular", 35)
    cta_text = "Get Hints & Solutions"
    cta_width, _ = get_text_dimensions(draw, cta_text, cta_font)
    draw.text((text_x_center - cta_width//2, 340), cta_text, font=cta_font, fill=(255, 255, 200))
    
    # Website
    brand_font = get_font("bold", 40)
    brand_text = "wordsolverx.com"
    brand_width, _ = get_text_dimensions(draw, brand_text, brand_font)
    
    # Add background pill for website
    pill_padding = 20
    pill_x = text_x_center - brand_width//2 - pill_padding
    pill_y = 440
    draw.rounded_rectangle([pill_x, pill_y, pill_x + brand_width + pill_padding*2, pill_y + 60], 
                          radius=30, fill=(255, 255, 255, 50))
    draw.text((text_x_center - brand_width//2, pill_y + 10), brand_text, 
             font=brand_font, fill="white")
    
    # Divider line between icon and text
    draw.line([(480, 100), (480, height - 100)], fill=(255, 255, 255, 80), width=2)
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='_facebook.png', delete=False)
    img.save(temp_file.name, 'PNG', quality=95)
    print(f"Generated Facebook image: {temp_file.name}")
    
    return temp_file.name


def generate_pin_image(puzzle_name, date_str, primary_color=None, gradient_colors=None):
    """
    Legacy function for backward compatibility.
    Generates Pinterest image.
    """
    return generate_pinterest_image(puzzle_name, date_str, gradient_colors)


def generate_images_for_all_platforms(puzzle_name, date_str):
    """
    Generate images for both Pinterest and Facebook.
    
    Returns:
        dict: {"pinterest": path, "facebook": path}
    """
    return {
        "pinterest": generate_pinterest_image(puzzle_name, date_str),
        "facebook": generate_facebook_image(puzzle_name, date_str)
    }


if __name__ == "__main__":
    # Test image generation for all puzzle types
    puzzles = ["Wordle", "Quordle", "Colordle", "Semantle", "Phoodle"]
    date_str = "January 17, 2026"
    
    for puzzle in puzzles:
        print(f"\n--- Generating images for {puzzle} ---")
        paths = generate_images_for_all_platforms(puzzle, date_str)
        print(f"Pinterest: {paths['pinterest']}")
        print(f"Facebook: {paths['facebook']}")
    
    print("\n✅ All test images generated successfully!")
