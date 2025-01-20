import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime, timedelta
import os
import subprocess

# Parse command-line arguments first
parser = argparse.ArgumentParser()
parser.add_argument("--start-color", type=str, required=True, help="Start color (R,G,B)")
parser.add_argument("--end-color", type=str, required=True, help="End color (R,G,B)")
parser.add_argument("--width", type=int, required=True, help="Screen width")
parser.add_argument("--height", type=int, required=True, help="Screen height")
parser.add_argument("--message", type=str, default="Happy New Year!", help="Custom message")
parser.add_argument("--output-folder", type=str, required=True, help="Output folder for images")

args = parser.parse_args()

# Now set the resolution after parsing
WIDTH, HEIGHT = args.width, args.height
FONT_SIZE = 60  # Smaller text size for a techy look
DOT_RADIUS = 12  # Dot size
DOT_SPACING = 30  # Spacing between dots

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_GRAY = (150, 150, 150)

# Function to draw a blurred shrinking circle
def draw_shrinking_circle(img, day, total_days, start_color, end_color):
    max_radius = WIDTH // 2
    min_radius = WIDTH // 8
    circle_radius = max_radius - (day / total_days) * (max_radius - min_radius)

    # Interpolate colors
    r = start_color[0] + (end_color[0] - start_color[0]) * (day / total_days)
    g = start_color[1] + (end_color[1] - start_color[1]) * (day / total_days)
    b = start_color[2] + (end_color[2] - start_color[2]) * (day / total_days)
    alpha_value = int(250 - (day / total_days) * 80)

    circle_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_img)

    center_x, center_y = WIDTH // 2, HEIGHT // 2
    circle_draw.ellipse(
        (center_x - circle_radius, center_y - circle_radius, 
         center_x + circle_radius, center_y + circle_radius), 
        fill=(int(r), int(g), int(b), alpha_value)
    )

    blurred_circle = circle_img.filter(ImageFilter.GaussianBlur(120))
    img.paste(blurred_circle, (0, 0), blurred_circle)

def generate_countdown_images(start_color, end_color, custom_message, output_folder):
    start_of_year = datetime(datetime.today().year, 1, 1)
    end_of_year = datetime(datetime.today().year, 12, 31)
    total_days = (end_of_year - start_of_year).days + 1

    dot_positions = [(row, col) for row in range(23) for col in range(16)]
    dot_positions = dot_positions[:365]  # Ensure exactly 365 dots

    for day in range(total_days):
        current_day = start_of_year + timedelta(days=day)
        days_left = total_days - day - 1
        percent_left = (days_left / total_days) * 100

        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)

        draw_shrinking_circle(img, day, total_days, start_color, end_color)

        # Draw grid
        grid_width = 16 * (DOT_RADIUS * 2 + DOT_SPACING)
        grid_height = 23 * (DOT_RADIUS * 2 + DOT_SPACING)
        start_x = (WIDTH - grid_width) // 2
        start_y = (HEIGHT - grid_height) // 2

        for i, (row, col) in enumerate(dot_positions):
            color = GRAY if i < day else WHITE
            x = start_x + col * (DOT_RADIUS * 2 + DOT_SPACING)
            y = start_y + row * (DOT_RADIUS * 2 + DOT_SPACING)
            draw.ellipse([x, y, x + DOT_RADIUS * 2, y + DOT_RADIUS * 2], fill=color)

        # Load font
        font_path = "/System/Library/Fonts/Supplemental/Menlo.ttc"
        font_large = ImageFont.truetype(font_path, FONT_SIZE)
        font_small = ImageFont.truetype(font_path, 40)

        # Add year in bottom left corner
        text_year = f"{current_day.year}"
        year_bbox = draw.textbbox((0, 0), text_year, font=font_large)
        draw.text((50, HEIGHT - 150), text_year, font=font_large, fill=WHITE)

        # Add percentage left in bottom right corner
        text_percent_left = f"{percent_left:.1f}% left" if day < total_days - 1 else "Happy New Year!"
        percent_bbox = draw.textbbox((0, 0), text_percent_left, font=font_large)
        draw.text((WIDTH - percent_bbox[2] - 50, HEIGHT - 150), text_percent_left, font=font_large, fill=DARK_GRAY)

        # Center the custom message under the grid
        message_bbox = draw.textbbox((0, 0), custom_message, font=font_small)
        message_x = (WIDTH - message_bbox[2]) // 2
        draw.text((message_x, start_y + grid_height + 30), custom_message, font=font_small, fill=WHITE)

        # Save the image
        filename = os.path.join(output_folder, f"countdown_{current_day.strftime('%Y-%m-%d')}.png")
        img.save(filename)

        mod_time = current_day.timestamp()
        os.utime(filename, (mod_time, mod_time))
        subprocess.run(["SetFile", "-d", current_day.strftime('%m/%d/%Y %H:%M:%S'), filename])

        print(f"Image saved: {filename}")

if __name__ == "__main__":
    start_color = tuple(map(int, args.start_color.split(',')))
    end_color = tuple(map(int, args.end_color.split(',')))

    generate_countdown_images(start_color, end_color, args.message, args.output_folder)