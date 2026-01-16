"""
Image Generator for Pinterest Pins
Creates attractive images with puzzle name and date
"""

from PIL import Image, ImageDraw, ImageFont
import os
import tempfile

def generate_pin_image(puzzle_name, date_str, primary_color="#6aaa64", gradient_colors=None):
    """
    Generate an attractive pin image for a puzzle.
    
    Args:
        puzzle_name: Name of the puzzle (e.g., "Wordle")
        date_str: Formatted date string (e.g., "January 17, 2026")
        primary_color: Main color hex code
        gradient_colors: List of two colors for gradient [start, end]
    
    Returns:
        Path to the generated image file
    """
    # Pinterest recommended size: 1000x1500 (2:3 ratio)
    width, height = 1000, 1500
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    if gradient_colors and len(gradient_colors) == 2:
        start_color = hex_to_rgb(gradient_colors[0])
        end_color = hex_to_rgb(gradient_colors[1])
    else:
        start_color = hex_to_rgb(primary_color)
        end_color = darken_color(start_color, 0.3)
    
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add decorative elements
    draw_decorations(draw, width, height, primary_color)
    
    # Load fonts (use default if custom not available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 80)
        date_font = ImageFont.truetype("arial.ttf", 50)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        date_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw text
    # Main title: "{Puzzle} Answer"
    title_text = f"{puzzle_name} Answer"
    draw_centered_text(draw, title_text, width, 550, title_font, "white", shadow=True)
    
    # Subtitle: "for"
    draw_centered_text(draw, "for", width, 650, subtitle_font, (200, 200, 200))
    
    # Date
    draw_centered_text(draw, date_str, width, 720, date_font, "white", shadow=True)
    
    # Website
    draw_centered_text(draw, "wordsolverx.com", width, 1350, subtitle_font, (230, 230, 230))
    
    # Add puzzle icon/symbol
    draw_puzzle_icon(draw, width, height, puzzle_name)
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG', quality=95)
    print(f"Generated image: {temp_file.name}")
    
    return temp_file.name

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def darken_color(rgb, factor):
    """Darken an RGB color by a factor (0-1)"""
    return tuple(int(c * (1 - factor)) for c in rgb)

def draw_centered_text(draw, text, width, y, font, color, shadow=False):
    """Draw text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    
    if shadow:
        # Draw shadow
        draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0, 128))
    
    draw.text((x, y), text, font=font, fill=color)

def draw_decorations(draw, width, height, primary_color):
    """Add decorative elements to the image"""
    # Add subtle pattern overlay
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            if (i + j) % 100 == 0:
                draw.ellipse([i-5, j-5, i+5, j+5], fill=(255, 255, 255, 20))
    
    # Add corner accents
    accent_size = 150
    draw.polygon([(0, 0), (accent_size, 0), (0, accent_size)], fill=(255, 255, 255, 30))
    draw.polygon([(width, height), (width - accent_size, height), (width, height - accent_size)], fill=(255, 255, 255, 30))

def draw_puzzle_icon(draw, width, height, puzzle_name):
    """Draw a simple icon for the puzzle type"""
    center_x = width // 2
    icon_y = 300
    box_size = 60
    gap = 10
    
    if puzzle_name.lower() == "wordle":
        # 5 boxes in a row
        start_x = center_x - (5 * box_size + 4 * gap) // 2
        colors = ["#6aaa64", "#c9b458", "#6aaa64", "#6aaa64", "#c9b458"]
        for i, color in enumerate(colors):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, icon_y, x + box_size, icon_y + box_size], radius=8, fill=color)
    
    elif puzzle_name.lower() == "quordle":
        # 2x2 grid
        start_x = center_x - (2 * box_size + gap) // 2
        colors = ["#6aaa64", "#c9b458", "#787c7e", "#6aaa64"]
        for i in range(4):
            row, col = i // 2, i % 2
            x = start_x + col * (box_size + gap)
            y = icon_y + row * (box_size + gap)
            draw.rounded_rectangle([x, y, x + box_size, y + box_size], radius=8, fill=colors[i])
    
    elif puzzle_name.lower() == "colordle":
        # Color spectrum boxes
        start_x = center_x - (5 * box_size + 4 * gap) // 2
        colors = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#3498db"]
        for i, color in enumerate(colors):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, icon_y, x + box_size, icon_y + box_size], radius=8, fill=color)
    
    elif puzzle_name.lower() == "semantle":
        # Gradient boxes representing similarity
        start_x = center_x - (5 * box_size + 4 * gap) // 2
        for i in range(5):
            x = start_x + i * (box_size + gap)
            intensity = int(255 * (i + 1) / 5)
            color = (52, 152, 219, intensity)
            draw.rounded_rectangle([x, icon_y, x + box_size, icon_y + box_size], radius=8, fill=f"#{intensity:02x}{intensity:02x}ff")
    
    elif puzzle_name.lower() == "phoodle":
        # Food-themed boxes
        start_x = center_x - (5 * box_size + 4 * gap) // 2
        colors = ["#e67e22", "#f39c12", "#27ae60", "#e74c3c", "#f1c40f"]
        for i, color in enumerate(colors):
            x = start_x + i * (box_size + gap)
            draw.rounded_rectangle([x, icon_y, x + box_size, icon_y + box_size], radius=8, fill=color)

if __name__ == "__main__":
    # Test image generation
    test_path = generate_pin_image(
        puzzle_name="Wordle",
        date_str="January 17, 2026",
        primary_color="#6aaa64",
        gradient_colors=["#6aaa64", "#538d4e"]
    )
    print(f"Test image saved to: {test_path}")
