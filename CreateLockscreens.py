from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime, timedelta
import os
import subprocess

# iPhone 11 Pro Max resolution
WIDTH, HEIGHT = 1242, 2688
FONT_SIZE = 60  # Smaller text size for a techy look
DOT_RADIUS = 12  # Dot size
DOT_SPACING = 30  # Spacing between dots

# Colors
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# Function to draw a blurred shrinking circle with controlled brightness
def draw_shrinking_circle(img, day, total_days):
    max_radius = WIDTH // 2
    min_radius = WIDTH // 8
    circle_radius = max_radius - (day / total_days) * (max_radius - min_radius)

    # Color shifting logic: maintain vibrancy, prevent dull grays
    start_color = (80, 120, 255)  # Vibrant blue at the start
    end_color = (40, 90, 200)     # Slightly darker but still vibrant blue

    # Calculate color interpolation
    r = start_color[0] + (end_color[0] - start_color[0]) * (day / total_days)
    g = start_color[1] + (end_color[1] - start_color[1]) * (day / total_days)
    b = start_color[2] + (end_color[2] - start_color[2]) * (day / total_days)

    alpha_value = int(250 - (day / total_days) * 80)  # Maintain some transparency but not too much

    circle_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_img)

    center_x, center_y = WIDTH // 2, HEIGHT // 2
    circle_draw.ellipse(
        (center_x - circle_radius, center_y - circle_radius, 
         center_x + circle_radius, center_y + circle_radius), 
        fill=(int(r), int(g), int(b), alpha_value)  # Smooth color transition with consistent vibrancy
    )

    # Apply Gaussian blur for a soft glow effect
    blurred_circle = circle_img.filter(ImageFilter.GaussianBlur(120))
    img.paste(blurred_circle, (0, 0), blurred_circle)

def generate_countdown_images():
    start_of_year = datetime(datetime.today().year, 1, 1)
    end_of_year = datetime(datetime.today().year, 12, 31)
    total_days = (end_of_year - start_of_year).days + 1

    dot_positions = [(row, col) for row in range(23) for col in range(16)]  # Ensure exactly 365 dots
    dot_positions = dot_positions[:365]  # Trim to exact number

    for day in range(total_days):
        current_day = start_of_year + timedelta(days=day)
        days_left = total_days - day - 1  # Adjusted to properly reflect days left
        percent_left = (days_left / total_days) * 100  # Inverted percentage

        # Create a blank black image
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)

        # Draw shrinking circle background effect
        draw_shrinking_circle(img, day, total_days)

        # Adjust grid to be centered and fit within a nice rectangle
        grid_width = 16 * (DOT_RADIUS * 2 + DOT_SPACING)
        grid_height = 23 * (DOT_RADIUS * 2 + DOT_SPACING)

        start_x = (WIDTH - grid_width) // 2
        start_y = (HEIGHT - grid_height) // 2  # Position higher on screen

        for i, (row, col) in enumerate(dot_positions):
            color = GRAY if i < day else WHITE
            x = start_x + col * (DOT_RADIUS * 2 + DOT_SPACING)
            y = start_y + row * (DOT_RADIUS * 2 + DOT_SPACING)
            draw.ellipse([x, y, x + DOT_RADIUS * 2, y + DOT_RADIUS * 2], fill=color)

        # Load a techy font
        font_path = "/System/Library/Fonts/Supplemental/Menlo.ttc"
        font = ImageFont.truetype(font_path, FONT_SIZE)

        # Bottom left text: Year
        text_year = f"{current_day.year}"
        draw.text((50, HEIGHT - 200), text_year, font=font, fill=WHITE)

        # Bottom right text: Percentage left
        if day == total_days - 1:
            text_percent_left = "Happy New Year!"
        else:
            text_percent_left = f"{percent_left:.1f}% left"
        percent_bbox = draw.textbbox((0, 0), text_percent_left, font=font)
        draw.text((WIDTH - percent_bbox[2] - 50, HEIGHT - 200), text_percent_left, font=font, fill=DARK_GRAY)

        # Save the image
        filename = f"countdown_{current_day.strftime('%Y-%m-%d')}.png"
        img.save(filename)

        # Set file creation and modification times to the date the PNG represents
        mod_time = current_day.timestamp()
        os.utime(filename, (mod_time, mod_time))
        subprocess.run(["SetFile", "-d", current_day.strftime('%m/%d/%Y %H:%M:%S'), filename])
        
        print(f"Image saved as {filename} with creation date {current_day.strftime('%Y-%m-%d')} set correctly")

generate_countdown_images()
