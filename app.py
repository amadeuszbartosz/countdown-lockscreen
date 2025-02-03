import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from PIL import Image, ImageDraw, ImageTk, ImageFilter, ImageFont, ImageFilter
import subprocess, os, sys, logging, argparse
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# ----------------------- Backend Logic (Image Generation) -----------------------
FONT_SIZE = 60
DOT_RADIUS = 12
DOT_SPACING = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_GRAY = (150, 150, 150)

def draw_shrinking_circle(img, day, total_days, start_color, end_color, WIDTH, HEIGHT):
    max_radius = WIDTH // 2
    min_radius = WIDTH // 8
    circle_radius = max_radius - (day / total_days) * (max_radius - min_radius)
    r = start_color[0] + (end_color[0] - start_color[0]) * (day / total_days)
    g = start_color[1] + (end_color[1] - start_color[1]) * (day / total_days)
    b = start_color[2] + (end_color[2] - start_color[2]) * (day / total_days)
    alpha_value = int(250 - (day / total_days) * 80)
    circle_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_img)
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    circle_draw.ellipse((center_x - circle_radius, center_y - circle_radius,
                         center_x + circle_radius, center_y + circle_radius),
                         fill=(int(r), int(g), int(b), alpha_value))
    blurred_circle = circle_img.filter(ImageFilter.GaussianBlur(120))
    img.paste(blurred_circle, (0, 0), blurred_circle)

def generate_countdown_images(start_color, end_color, custom_message, output_folder, WIDTH, HEIGHT):
    start_of_year = datetime(datetime.today().year, 1, 1)
    end_of_year = datetime(datetime.today().year, 12, 31)
    total_days = (end_of_year - start_of_year).days + 1
    dot_positions = [(row, col) for row in range(23) for col in range(16)]
    dot_positions = dot_positions[:365]
    for day in range(total_days):
        current_day = start_of_year + timedelta(days=day)
        days_left = total_days - day - 1
        percent_left = (days_left / total_days) * 100
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)
        draw_shrinking_circle(img, day, total_days, start_color, end_color, WIDTH, HEIGHT)
        grid_width = 16 * (DOT_RADIUS * 2 + DOT_SPACING)
        grid_height = 23 * (DOT_RADIUS * 2 + DOT_SPACING)
        start_x = (WIDTH - grid_width) // 2
        start_y = (HEIGHT - grid_height) // 2
        for i, (row, col) in enumerate(dot_positions):
            color = GRAY if i < day else WHITE
            x = start_x + col * (DOT_RADIUS * 2 + DOT_SPACING)
            y = start_y + row * (DOT_RADIUS * 2 + DOT_SPACING)
            draw.ellipse([x, y, x + DOT_RADIUS * 2, y + DOT_RADIUS * 2], fill=color)
        font_path = "/System/Library/Fonts/Supplemental/Menlo.ttc"
        font_large = ImageFont.truetype(font_path, FONT_SIZE)
        font_small = ImageFont.truetype(font_path, 40)
        text_year = f"{current_day.year}"
        draw.text((50, HEIGHT - 150), text_year, font=font_large, fill=WHITE)
        text_percent_left = f"{percent_left:.1f}% left" if day < total_days - 1 else "Happy New Year!"
        percent_bbox = draw.textbbox((0, 0), text_percent_left, font=font_large)
        x_text = WIDTH - percent_bbox[2] - 50
        if x_text < 0:  # ensure text isn't cut off
            x_text = 0
        draw.text((x_text, HEIGHT - 150), text_percent_left, font=font_large, fill=DARK_GRAY)
        message_bbox = draw.textbbox((0, 0), custom_message, font=font_small)
        message_x = (WIDTH - message_bbox[2]) // 2
        draw.text((message_x, start_y + grid_height + 30), custom_message, font=font_small, fill=WHITE)
        filename = os.path.join(output_folder, f"countdown_{current_day.strftime('%Y-%m-%d')}.png")
        img.save(filename)
        if sys.platform.startswith("darwin"):
            # Set both created (-d) and modified (-m) dates on macOS
            formatted_date = current_day.strftime('%m/%d/%Y %H:%M:%S')
            subprocess.run(["SetFile", "-d", formatted_date, filename])
            subprocess.run(["SetFile", "-m", formatted_date, filename])
        else:
            os.utime(filename, (current_day.timestamp(), current_day.timestamp()))
        print(f"Image saved: {filename}")

# --------------------------- GUI Logic ---------------------------
def create_color_circle(color_hex, size=(150, 150)):
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)
    draw.ellipse((0, 0, size[0], size[1]), fill=(r, g, b, 200))
    img = img.filter(ImageFilter.GaussianBlur(30))
    return ImageTk.PhotoImage(img)

def pick_color(canvas):
    color = colorchooser.askcolor()[1]
    if color:
        blurred_image = create_color_circle(color)
        canvas.color_hex = color
        canvas.create_image(0, 0, anchor=tk.NW, image=blurred_image)
        canvas.image = blurred_image

def select_directory():
    folder_selected = filedialog.askdirectory(title="Select Save Location")
    if folder_selected:
        folder_name = folder_selected.split("/")[-1]
        folder_var.set(folder_name)
        full_folder_path.set(folder_selected)
        generate_button.config(state="normal")

def generate_images():
    folder = full_folder_path.get()
    start_color_hex = start_canvas.color_hex.lstrip('#')
    end_color_hex = end_canvas.color_hex.lstrip('#')
    message = message_entry.get()
    phone_model = selected_phone.get()
    width, height = phone_options[phone_model]
    if not folder or not start_color_hex or not end_color_hex:
        messagebox.showwarning("Warning", "Please fill all fields before generating images.")
        return
    # Convert HEX to RGB tuple
    start_color = (int(start_color_hex[:2], 16), int(start_color_hex[2:4], 16), int(start_color_hex[4:], 16))
    end_color = (int(end_color_hex[:2], 16), int(end_color_hex[2:4], 16), int(end_color_hex[4:], 16))
    logging.debug("Starting image generation...")
    try:
        generate_countdown_images(start_color, end_color, message, folder, width, height)
        messagebox.showinfo("Success", "Countdown images have been generated successfully!")
    except subprocess.CalledProcessError as e:
        extra = ""
        if sys.platform.startswith("darwin"):
            extra = "\nIf you see an error about unverified software, please open System Preferences > Security & Privacy > General and click 'Allow Anyway'."
        logging.error(f"Subprocess failed: {e.stderr}")
        messagebox.showerror("Error", f"Failed to generate images.\n{e.stderr}{extra}")
    except Exception as e:
        extra = ""
        if sys.platform.startswith("darwin"):
            extra = "\nIf you see an error about unverified software, please open System Preferences > Security & Privacy > General and click 'Allow Anyway'."
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}{extra}")

def launch_gui():
    global root, start_canvas, end_canvas, folder_var, full_folder_path, message_entry, generate_button, phone_options, selected_phone
    root = ttkb.Window(themename="darkly")
    root.title("Countdown Lockscreen Customizer")
    root.geometry("600x650")
    root.resizable(False, False)
    ttkb.Label(root, text="Customize Your Countdown", font=("Menlo", 22, "bold"), bootstyle="inverse-primary").pack(pady=20)
    color_frame = ttkb.Frame(root)
    color_frame.pack(pady=10, padx=20)
    ttkb.Label(color_frame, text="Start Color:", font=("Menlo", 12), bootstyle="inverse-primary").grid(row=0, column=0, padx=40)
    start_canvas = tk.Canvas(color_frame, width=150, height=150, bg="black", highlightthickness=0)
    start_canvas.grid(row=1, column=0, padx=40)
    start_canvas.color_hex = "#ffffff"
    ttkb.Button(color_frame, text="Pick Start Color", command=lambda: pick_color(start_canvas), bootstyle="primary-outline").grid(row=2, column=0, pady=5)
    ttkb.Label(color_frame, text="End Color:", font=("Menlo", 12), bootstyle="inverse-primary").grid(row=0, column=1, padx=40)
    end_canvas = tk.Canvas(color_frame, width=150, height=150, bg="black", highlightthickness=0)
    end_canvas.grid(row=1, column=1, padx=40)
    end_canvas.color_hex = "#000000"
    ttkb.Button(color_frame, text="Pick End Color", command=lambda: pick_color(end_canvas), bootstyle="primary-outline").grid(row=2, column=1, pady=5)
    ttkb.Label(root, text="Select Phone Model:", font=("Menlo", 12), bootstyle="inverse-primary").pack(pady=5)
    phone_options = {
        "iPhone SE (2nd & 3rd Gen)": (750, 1334),
        "iPhone X / XS / 11 Pro": (1125, 2436),
        "iPhone XR / 11": (828, 1792),
        "iPhone XS Max / 11 Pro Max": (1242, 2688),
        "iPhone 12 / 12 Pro": (1170, 2532),
        "iPhone 12 Mini": (1080, 2340),
        "iPhone 12 Pro Max": (1284, 2778),
        "iPhone 13 Mini": (1080, 2340),
        "iPhone 13 / 13 Pro": (1170, 2532),
        "iPhone 13 Pro Max": (1284, 2778),
        "iPhone 14 / 14 Pro": (1179, 2556),
        "iPhone 14 Plus": (1284, 2778),
        "iPhone 14 Pro Max": (1290, 2796),
        "iPhone 15 / 15 Pro": (1179, 2556),
        "iPhone 15 Plus": (1290, 2796),
        "iPhone 15 Pro Max": (1290, 2796),
        "Pixel 4a": (1080, 2340),
        "Pixel 5": (1080, 2340),
        "Pixel 6": (1080, 2400),
        "Pixel 6 Pro": (1440, 3120),
        "Pixel 7": (1080, 2400),
        "Pixel 7 Pro": (1440, 3120),
        "Pixel 8": (1080, 2400),
        "Pixel 8 Pro": (1344, 2992),
        "Samsung Galaxy S20": (1440, 3200),
        "Samsung Galaxy S20+": (1440, 3200),
        "Samsung Galaxy S20 Ultra": (1440, 3200),
        "Samsung Galaxy S21": (1080, 2400),
        "Samsung Galaxy S21+": (1080, 2400),
        "Samsung Galaxy S21 Ultra": (1440, 3200),
        "Samsung Galaxy S22": (1080, 2340),
        "Samsung Galaxy S22+": (1080, 2340),
        "Samsung Galaxy S22 Ultra": (1440, 3088),
        "Samsung Galaxy S23": (1080, 2340),
        "Samsung Galaxy S23+": (1080, 2340),
        "Samsung Galaxy S23 Ultra": (1440, 3088),
        "OnePlus 8": (1080, 2400),
        "OnePlus 8 Pro": (1440, 3168),
        "OnePlus 9": (1080, 2400),
        "OnePlus 9 Pro": (1440, 3216),
        "OnePlus 10 Pro": (1440, 3216)
    }
    selected_phone = tk.StringVar(value="iPhone 15 Pro Max")
    phone_dropdown = ttkb.Combobox(root, textvariable=selected_phone, values=list(phone_options.keys()), font=("Menlo", 12), bootstyle="dark")
    phone_dropdown.pack(pady=5, padx=40, fill=tk.X)
    ttkb.Label(root, text="Custom Message:", font=("Menlo", 12), bootstyle="inverse-primary").pack(pady=5)
    message_var = tk.StringVar()
    message_entry = ttkb.Entry(root, textvariable=message_var, font=("Menlo", 12), bootstyle="dark")
    message_entry.pack(pady=5, padx=40, fill=tk.X)
    ttkb.Label(root, text="Save to:", font=("Menlo", 12), bootstyle="inverse-primary").pack(pady=5)
    folder_var = tk.StringVar()
    full_folder_path = tk.StringVar()
    folder_display = ttkb.Entry(root, textvariable=folder_var, font=("Menlo", 12), bootstyle="dark", state="readonly")
    folder_display.pack(pady=5, padx=40, fill=tk.X)
    ttkb.Button(root, text="Choose Folder", command=select_directory, bootstyle="primary").pack(pady=5)
    global generate_button
    generate_button = ttkb.Button(root, text="Generate Images", command=generate_images, bootstyle="success", state="disabled")
    generate_button.pack(pady=20, padx=40, fill=tk.X)
    root.mainloop()

# ------------------------------ Main Entry --------------------------------
if __name__ == "__main__":
    # If command-line arguments are provided, assume backend mode:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-color", type=str, help="Start color (R,G,B)")
    parser.add_argument("--end-color", type=str, help="End color (R,G,B)")
    parser.add_argument("--width", type=int, help="Screen width")
    parser.add_argument("--height", type=int, help="Screen height")
    parser.add_argument("--message", type=str, help="Custom message", default="Happy New Year!")
    parser.add_argument("--output-folder", type=str, help="Output folder for images")
    args, unknown = parser.parse_known_args()
    # If required backend args are present, run image generation:
    if args.start_color and args.end_color and args.width and args.height and args.output_folder:
        start_color = tuple(map(int, args.start_color.split(',')))
        end_color = tuple(map(int, args.end_color.split(',')))
        generate_countdown_images(start_color, end_color, args.message, args.output_folder, args.width, args.height)
    else:
        # Otherwise start the GUI
        launch_gui()