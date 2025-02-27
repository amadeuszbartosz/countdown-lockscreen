import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import subprocess
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a blurred circular preview
def create_color_circle(color_hex, size=(150, 150)):
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)

    # Draw filled circle with gradient effect
    radius = size[0] // 2
    draw.ellipse((0, 0, size[0], size[1]), fill=(r, g, b, 200))

    # Apply Gaussian blur
    img = img.filter(ImageFilter.GaussianBlur(30))

    return ImageTk.PhotoImage(img)

# Function to update color preview with Gaussian blurred circle
def pick_color(canvas):
    color = colorchooser.askcolor()[1]
    if color:
        blurred_image = create_color_circle(color)
        canvas.color_hex = color  # Store the HEX value
        canvas.create_image(0, 0, anchor=tk.NW, image=blurred_image)
        canvas.image = blurred_image  # Keep reference to avoid garbage collection

# Function to select directory and show only the final folder name
def select_directory():
    folder_selected = filedialog.askdirectory(title="Select Save Location")
    if folder_selected:
        folder_name = folder_selected.split("/")[-1]
        folder_var.set(folder_name)
        full_folder_path.set(folder_selected)
        generate_button.config(state="normal")

def generate_images():
    folder = full_folder_path.get()
    start_color = start_canvas.color_hex.lstrip('#')
    end_color = end_canvas.color_hex.lstrip('#')
    message = message_entry.get()
    phone_model = selected_phone.get()
    width, height = phone_options[phone_model]

    if not folder or not start_color or not end_color:
        messagebox.showwarning("Warning", "Please fill all fields before generating images.")
        return

    try:
        # Determine the backend executable/script path:
        if getattr(sys, 'frozen', False):
            # Go up three levels from the GUI executable inside Countdown Creator.app
            base_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "..", "..", ".."))
            backend_path = os.path.join(
                base_path,
                "CreateLockScreens.app",
                "Contents",
                "MacOS",
                "CreateLockScreens"
            )
        else:
            # In development, use the Python script.
            backend_path = "CreateLockScreens.py"
        
        logging.debug(f"Backend path: {backend_path}")
        
        # Choose command based on the backend type.
        if backend_path.endswith(".py"):
            command = [
                sys.executable, backend_path,
                "--start-color", f"{int(start_color[:2], 16)},{int(start_color[2:4], 16)},{int(start_color[4:], 16)}",
                "--end-color", f"{int(end_color[:2], 16)},{int(end_color[2:4], 16)},{int(end_color[4:], 16)}",
                "--message", message,
                "--output-folder", folder,
                "--width", str(width),
                "--height", str(height)
            ]
        else:
            # Backend is an executable.
            command = [
                backend_path,
                "--start-color", f"{int(start_color[:2], 16)},{int(start_color[2:4], 16)},{int(start_color[4:], 16)}",
                "--end-color", f"{int(end_color[:2], 16)},{int(end_color[2:4], 16)},{int(end_color[4:], 16)}",
                "--message", message,
                "--output-folder", folder,
                "--width", str(width),
                "--height", str(height)
            ]
        
        logging.debug(f"Command: {command}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        logging.debug(f"Result: {result.stdout}")
        messagebox.showinfo("Success", "Countdown images have been generated successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess failed: {e.stderr}")
        messagebox.showerror("Error", f"Failed to generate images.\n{e.stderr}")
        print("Error:", e.stderr)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")
        print("Error:", e)

# Create main window
root = ttkb.Window(themename="darkly")
root.title("Countdown Lockscreen Customizer")
root.geometry("600x650")
root.resizable(False, False)

# Title
ttkb.Label(root, text="Customize Your Countdown", font=("Menlo", 22, "bold"), bootstyle="inverse-primary").pack(pady=20)

# Color Picker Section (Centered)
color_frame = ttkb.Frame(root)
color_frame.pack(pady=10, padx=20)

# Start Color Section
ttkb.Label(color_frame, text="Start Color:", font=("Menlo", 12), bootstyle="inverse-primary").grid(row=0, column=0, padx=40)
start_canvas = tk.Canvas(color_frame, width=150, height=150, bg="black", highlightthickness=0)
start_canvas.grid(row=1, column=0, padx=40)
start_canvas.color_hex = "#ffffff"  # Default color
ttkb.Button(color_frame, text="Pick Start Color", command=lambda: pick_color(start_canvas), bootstyle="primary-outline").grid(row=2, column=0, pady=5)

# End Color Section
ttkb.Label(color_frame, text="End Color:", font=("Menlo", 12), bootstyle="inverse-primary").grid(row=0, column=1, padx=40)
end_canvas = tk.Canvas(color_frame, width=150, height=150, bg="black", highlightthickness=0)
end_canvas.grid(row=1, column=1, padx=40)
end_canvas.color_hex = "#000000"  # Default color
ttkb.Button(color_frame, text="Pick End Color", command=lambda: pick_color(end_canvas), bootstyle="primary-outline").grid(row=2, column=1, pady=5)

# Add a dropdown for phone selection
ttkb.Label(root, text="Select Phone Model:", font=("Menlo", 12), bootstyle="inverse-primary").pack(pady=5)
phone_options = {
    # 📱 iPhones
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

    # 📱 Google Pixel Devices
    "Pixel 4a": (1080, 2340),
    "Pixel 5": (1080, 2340),
    "Pixel 6": (1080, 2400),
    "Pixel 6 Pro": (1440, 3120),
    "Pixel 7": (1080, 2400),
    "Pixel 7 Pro": (1440, 3120),
    "Pixel 8": (1080, 2400),
    "Pixel 8 Pro": (1344, 2992),

    # 📱 Samsung Galaxy Devices
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

    # 📱 Other Popular Phones
    "OnePlus 8": (1080, 2400),
    "OnePlus 8 Pro": (1440, 3168),
    "OnePlus 9": (1080, 2400),
    "OnePlus 9 Pro": (1440, 3216),
    "OnePlus 10 Pro": (1440, 3216)
}
selected_phone = tk.StringVar(value="iPhone 11 Pro Max")
phone_dropdown = ttkb.Combobox(root, textvariable=selected_phone, values=list(phone_options.keys()), font=("Menlo", 12), bootstyle="dark")
phone_dropdown.pack(pady=5, padx=40, fill=X)

# Custom Message
ttkb.Label(root, text="Custom Message:", font=("Menlo", 12), bootstyle="inverse-primary").pack(pady=5)
message_var = tk.StringVar()
message_entry = ttkb.Entry(root, textvariable=message_var, font=("Menlo", 12), bootstyle="dark")
message_entry.pack(pady=5, padx=40, fill=X)

# Save Location
ttkb.Label(root, text="Save to:", font=("Menlo", 12), bootstyle="inverse-primary").pack(pady=5)
folder_var = tk.StringVar()
full_folder_path = tk.StringVar()
folder_display = ttkb.Entry(root, textvariable=folder_var, font=("Menlo", 12), bootstyle="dark", state="readonly")
folder_display.pack(pady=5, padx=40, fill=X)
ttkb.Button(root, text="Choose Folder", command=select_directory, bootstyle="primary").pack(pady=5)

# Generate Button
generate_button = ttkb.Button(root, text="Generate Images", command=generate_images, bootstyle="success", state="disabled")
generate_button.pack(pady=20, padx=40, fill=X)

# Run the main loop
root.mainloop()