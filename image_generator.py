"""
Professional Image Generator for Social Media
Creates attractive, readable images for Pinterest and Facebook
"""

from PIL import Image, ImageDraw, ImageFont
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


def get_text_dimensions(draw, text, font):
    """Get text width and height"""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_text_with_box(draw, text, center_x, center_y, font, text_color, box_color, padding_x=30, padding_y=15, radius=25):
    """Draw text inside a rounded rectangle box with precise centering"""
    # Use textbbox with anchor="mm" (middle-middle) to get precise dimensions relative to center
    bbox = draw.textbbox((center_x, center_y), text, font=font, anchor="mm")
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    
    # Calculate box coordinates from the text bbox with padding
    box_x1 = bbox[0] - padding_x
    box_y1 = bbox[1] - padding_y
    box_x2 = bbox[2] + padding_x
    box_y2 = bbox[3] + padding_y
    
    # Draw shadow for box
    shadow_offset = 6
    draw.rounded_rectangle(
        [box_x1 + shadow_offset, box_y1 + shadow_offset, box_x2 + shadow_offset, box_y2 + shadow_offset],
        radius=radius,
        fill=(0, 0, 0, 80)
    )
    
    # Draw main box
    draw.rounded_rectangle(
        [box_x1, box_y1, box_x2, box_y2],
        radius=radius,
        fill=box_color
    )
    
    # Draw text centered using anchor="mm"
    draw.text(
        (center_x, center_y),
        text,
        font=font,
        fill=text_color,
        anchor="mm"
    )
    
    # Return bottom Y of the box + padding for stacking
    return box_y2 + 20


def draw_puzzle_icon_large(draw, center_x, center_y, puzzle_name, box_size=120, gap=15):
    """Draw a large, prominent puzzle icon"""
    puzzle = puzzle_name.lower()
    
    if puzzle == "wordle":
        # 5 boxes in a row - Wordle style
        # Adjust size to fit 5 boxes in left panel
        if box_size < 80: box_size = 80
        if box_size > 90: box_size = 90  # Limit max size for 5-letter puzzles
            
        total_width = 5 * box_size + 4 * gap
        total_height = box_size
        start_x = center_x - total_width // 2
        start_y = center_y - total_height // 2
        
        colors = ["#6aaa64", "#c9b458", "#6aaa64", "#6aaa64", "#c9b458"]
        letters = ["W", "O", "R", "D", "S"]
        
        for i, (color, letter) in enumerate(zip(colors, letters)):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, start_y, x + box_size, start_y + box_size], 
                                   radius=15, fill=color)
            # Draw letter
            letter_font = get_font("bold", int(box_size * 0.6))
            draw.text((x + box_size//2, start_y + box_size//2), letter, 
                     font=letter_font, fill="white", anchor="mm")
    
    elif puzzle == "quordle":
        # 2x2 grid - Quordle style
        # Make very large as requested
        if box_size < 120: box_size = 120
            
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
                                   radius=15, fill=colors[i])
            letter_font = get_font("bold", int(box_size * 0.5))
            draw.text((x + box_size//2, y + box_size//2), letters[i], 
                     font=letter_font, fill="white", anchor="mm")
    
    elif puzzle == "colordle":
        # Rainbow color boxes
        if box_size < 80: box_size = 80
        if box_size > 90: box_size = 90
        
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        start_y = center_y - box_size // 2
        
        colors = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#3498db"]
        
        for i, color in enumerate(colors):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, start_y, x + box_size, start_y + box_size], 
                                   radius=15, fill=color, outline="white", width=4)
    
    elif puzzle == "semantle":
        # Gradient similarity boxes
        if box_size < 80: box_size = 80
        if box_size > 90: box_size = 90
        
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        start_y = center_y - box_size // 2
        
        for i in range(5):
            x = start_x + i * (box_size + gap)
            # Blue gradient from light to dark
            blue_intensity = int(100 + (155 * (i + 1) / 5))
            color = f"#3498db" if i == 4 else f"#{50+i*30:02x}{100+i*30:02x}{200+i*10:02x}"
            draw.rounded_rectangle([x, start_y, x + box_size, start_y + box_size], 
                                   radius=15, fill=color)
            if i == 4: # Top match (100)
                 # Pct text
                pct = "TOP"
                pct_font = get_font("bold", int(box_size * 0.3))
                draw.text((x + box_size//2, start_y + box_size//2), pct, 
                        font=pct_font, fill="white", anchor="mm")

    elif puzzle == "phoodle":
        # Food-themed colorful boxes
        if box_size < 80: box_size = 80
        if box_size > 90: box_size = 90
        
        total_width = 5 * box_size + 4 * gap
        start_x = center_x - total_width // 2
        start_y = center_y - box_size // 2
        
        colors = ["#e67e22", "#27ae60", "#e74c3c", "#f39c12", "#2ecc71"]
        letters = ["F", "O", "O", "D", "S"]
        
        for i, (color, letter) in enumerate(zip(colors, letters)):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, start_y, x + box_size, start_y + box_size], 
                                   radius=15, fill=color)
            letter_font = get_font("bold", int(box_size * 0.6))
            draw.text((x + box_size//2, start_y + box_size//2), letter, 
                     font=letter_font, fill="white", anchor="mm")


def generate_pinterest_image(puzzle_name, date_str, theme_colors=None):
    """
    Generate a professional Pinterest pin image with boxed text.
    Pinterest optimal size: 1000x1500
    """
    width, height = 1000, 1500
    
    # Theme colors
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
    
    # Background
    start_color = hex_to_rgb(theme["gradient"][0])
    end_color = hex_to_rgb(theme["gradient"][1])
    img = create_gradient(width, height, start_color, end_color)
    draw = ImageDraw.Draw(img)
    
    # Pattern
    for x in range(0, width, 60):
        for y in range(0, height, 60):
            draw.ellipse([x-4, y-4, x+4, y+4], fill=(255, 255, 255, 30))
    
    center_x = width // 2
    
    # 1. Puzzle Icon at Top
    draw_puzzle_icon_large(draw, center_x, 320, puzzle_name, box_size=110, gap=15)
    
    # 2. Main Title (White Box, Black Text)
    title_font = get_font("bold", 80)
    title_y = 600
    next_y = draw_text_with_box(draw, f"{puzzle_name} Answer", center_x, title_y, 
                      title_font, "black", "white", padding_x=40, padding_y=20, radius=30)
    
    # 3. "for" text (No Box)
    for_font = get_font("regular", 40)
    for_y = next_y + 30
    draw.text((center_x, for_y), "for", font=for_font, fill="white", anchor="mm")
    next_y = for_y + 40

    # 4. Date (Black Box, White Text)
    date_font = get_font("bold", 70)
    date_y = next_y + 60
    next_y = draw_text_with_box(draw, date_str, center_x, date_y, 
                      date_font, "white", "black", padding_x=40, padding_y=20, radius=30)
    
    # 5. Call to Action (Translucent Box)
    cta_font = get_font("semibold", 45)
    cta_y = next_y + 80
    cta_text = "Get Today's Hints & Answer"
    
    # Draw CTA box
    draw_text_with_box(draw, cta_text, center_x, cta_y, cta_font, 
                      (255, 255, 220), (0, 0, 0, 100), padding_x=30, padding_y=15, radius=25)

    # 6. Website Pill at Bottom
    brand_font = get_font("bold", 50)
    brand_y = 1380
    draw_text_with_box(draw, "wordsolverx.com", center_x, brand_y, 
                      brand_font, hex_to_rgb(theme["gradient"][1]), "white", 
                      padding_x=50, padding_y=25, radius=50)

    # Save
    temp_file = tempfile.NamedTemporaryFile(suffix='_pinterest.png', delete=False)
    img.save(temp_file.name, 'PNG', quality=95)
    print(f"Generated Pinterest image: {temp_file.name}")
    return temp_file.name


def generate_facebook_image(puzzle_name, date_str, theme_colors=None):
    """
    Generate professional Facebook image with split layout.
    Size: 1200x628
    """
    width, height = 1200, 628
    
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
    
    # Horizontal Gradient
    start_color = hex_to_rgb(theme["gradient"][0])
    end_color = hex_to_rgb(theme["gradient"][1])
    img = create_gradient(width, height, start_color, end_color, direction="horizontal")
    draw = ImageDraw.Draw(img)
    
    # Pattern
    for x in range(0, width, 50):
        for y in range(0, height, 50):
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 255, 30))
            
    # Layout Config
    divider_x = 550 # Moved right significantly per user request
    content_center_x = divider_x + (width - divider_x) // 2
    icon_center_x = divider_x // 2
    
    # 1. Full Height Divider
    draw.line([(divider_x, 0), (divider_x, height)], fill=(255, 255, 255, 120), width=4)

    # 2. Icon on Left Side (Large)
    # Reduce box size slightly for 5-letter puzzles in landscape mode
    box_size = 90 if puzzle_name.lower() in ["wordle", "phoodle", "colordle", "semantle"] else 110
    gap = 10 if puzzle_name.lower() in ["wordle", "phoodle", "colordle", "semantle"] else 15
    
    draw_puzzle_icon_large(draw, icon_center_x, height // 2, puzzle_name, box_size=box_size, gap=gap)
    
    # 3. Content on Right Side (Boxed Text)
    
    # Title: White Box, Black Text
    title_font = get_font("bold", 60)
    title_y = 130
    next_y = draw_text_with_box(draw, f"{puzzle_name} Answer", content_center_x, title_y,
                      title_font, "black", "white", padding_x=30, padding_y=15, radius=25)
    
    # Date: Black Box, White Text
    date_font = get_font("bold", 50)
    date_y = next_y + 70
    next_y = draw_text_with_box(draw, date_str, content_center_x, date_y,
                      date_font, "white", "black", padding_x=30, padding_y=15, radius=25)
                      
    # CTA Text (Translucent Box)
    cta_font = get_font("semibold", 35)
    cta_y = next_y + 70
    cta_text = "Get Hints & Solutions"
    draw_text_with_box(draw, cta_text, content_center_x, cta_y, cta_font, 
                      (255, 255, 220), (0, 0, 0, 80), padding_x=25, padding_y=12, radius=20)
    
    # Website Pill Box at Bottom Right
    brand_font = get_font("bold", 30)
    brand_y = 560
    draw_text_with_box(draw, "wordsolverx.com", content_center_x, brand_y,
                      brand_font, hex_to_rgb(theme["gradient"][1]), "white",
                      padding_x=30, padding_y=12, radius=30)

    # Save
    temp_file = tempfile.NamedTemporaryFile(suffix='_facebook.png', delete=False)
    img.save(temp_file.name, 'PNG', quality=95)
    print(f"Generated Facebook image: {temp_file.name}")
    return temp_file.name


def generate_pin_image(puzzle_name, date_str, primary_color=None, gradient_colors=None):
    """Legacy wrapper"""
    return generate_pinterest_image(puzzle_name, date_str, gradient_colors)


if __name__ == "__main__":
    # Test all puzzles
    puzzles = ["Wordle", "Quordle", "Colordle", "Semantle", "Phoodle"]
    date_str = "January 17, 2026"
    
    for puzzle in puzzles:
        print(f"\nGenering images for {puzzle}...")
        p = generate_pinterest_image(puzzle, date_str)
        f = generate_facebook_image(puzzle, date_str)
        print(f"Pinterest: {p}")
        print(f"Facebook: {f}")
