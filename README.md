# Countdown Lockscreen 📱

Welcome to the **Countdown Lockscreen** application. This tool generates 365 lock screen images for your iPhone, each displaying a countdown to the New Year with a dynamic dot grid and blurred circle effect.

---

## For Non-Developers
1. Go to the **Releases** section and download the latest version of the CountdownCreator Application.
2. Double-click the downloaded `CountdownCreator` app to launch it.
3. In the app, set the **start** and **end** colors, and enter a custom message if desired.
4. Choose an output folder where your images will be saved.
5. Once the images are generated, AirDrop them (or use your preferred method) and add them under a folder (for example, `countdown_photos`) on your device as shown in the screenshot.

---

## For Developers
- The new entry point is `app.py`. Old backend files (such as `CreateLockScreens.py` and `custom_gui.py`) can now be added to your `.gitignore`.
- Spec files are required for building executables and should not be ignored.
- To run or customize the project, open it in your IDE and modify `app.py` or the spec files as needed.
- Note: Shortcuts for other phone models aren’t fully set up yet, but you can still generate images for them.

---

## Features 🚀

- **Customizable Colors:** Choose your start and end colors for a dynamic gradient effect.
- **Device Compatibility:** Supports various iPhone models with different resolutions.
- **Daily Automation:** Automate wallpaper updates via iCloud and Shortcuts.
- **User-Friendly GUI:** Simple interface for generating countdown images.

---

## Setup Guide 🛠️

Follow these steps to download, run the executable, and automate the countdown wallpapers.

### 1. Download and Run the Executable 🖥️

1. Go to the **[Releases](https://github.com/yourrepo/countdown-lockscreen/releases)** page of this repository.
2. Download the latest version of the executable for your operating system:
   - **MacOS:** `CountdownLockscreen.dmg`
   - **Windows:** `CountdownLockscreen.exe`
3. Once downloaded, follow the steps below to run the application:

#### **On MacOS:**
1. Double-click the `.dmg` file to mount the disk image.
2. Drag the `CountdownLockscreen` app to the Applications folder.
3. Open the app (you may need to allow permissions under **System Preferences > Security & Privacy**).

#### **On Windows:**
1. Double-click the `CountdownLockscreen.exe` file to start the application.
2. If prompted, allow the app to run.

---

### 2. Generate Countdown Images 🖼️

1. Open the **Countdown Lockscreen** app.
2. Select your **start and end colors** for the countdown circle effect.
3. Choose your **iPhone model** from the dropdown menu.
4. Enter a **custom message** (optional) for the countdown display.
5. Click **"Choose Folder"** to select a location to save the generated images.
6. Press **"Generate Images"**, and the app will create 365 images named in the format:


---

### 3. Transfer Images to iPhone via AirDrop or Cloud ☁️

Once you've generated your countdown images, transfer them to your iPhone:

#### **Using AirDrop (Recommended for MacOS users):**
1. Select all the generated images in Finder. Right click, and compress them as a .zip
2. Right-click and choose **"Share" > "AirDrop"**.
3. Send the images to your iPhone.

#### **Using iCloud Drive:**
1. Move the generated images into your iCloud Drive.
2. Ensure they are placed inside a new folder named:
3. Open the Files app on your iPhone and confirm the images have synced.

---

### 4. Setting Up the iOS Shortcut 📲

To automatically update your lock screen daily, follow these steps:

1. Open the **Shortcuts** app on your iPhone.
2. Tap the **"+"** to create a new shortcut.
3. Add the action **"Get File from Folder"**:
- Folder: `countdown_photos`
- File Name: `countdown_📅 Current Date.png`
4. Add the action **"Set Wallpaper Photo"**:
- Set to: **Lock Screen**
- Select a wallpaper style.

📸 ![shortcut](https://github.com/user-attachments/assets/216a1a49-6a59-4557-b038-652b52219e10)

---

### 5. Automating the Wallpaper Update 🔄

Now, let's make sure the shortcut runs automatically every day.

1. Open the **Shortcuts** app and go to the **Automation** tab.
2. Tap **"+"** and select **"Create Personal Automation"**.
3. Choose **"Time of Day"** and set it to **12:00 AM** (or your preferred time).
4. Select **"Run Shortcut"**, then choose the countdown shortcut created earlier.
5. Disable **"Ask Before Running"** to ensure automation runs automatically.

📸 ![automation](https://github.com/user-attachments/assets/3b90bffa-b8a3-4b93-b749-3e17e577de23) 

---

## Countdown Lockscreen Example 📱

Below is an example of the generated countdown lockscreen in action on an iPhone.

<img src="https://github.com/user-attachments/assets/12582fac-4941-4dd8-8582-61b3ed476120" alt="final" width="500"/>

This lockscreen dynamically updates daily using the generated images stored in iCloud. The grid of dots represents the days left in the year, while the shrinking blurred circle changes color over time based on your selected gradient.

### Features:
- 📅 **Automatic daily updates** via iOS Shortcuts automation.
- 🎨 **Customizable gradient colors** to match your style.
- 📂 **Easy setup** with a simple GUI application to generate all images at once.
- 🕰️ **Accurate countdown visualization** with percentage and year indicators.

---

## Troubleshooting 🛠️

If you encounter any issues, try the following:

- Ensure all images are correctly named (`countdown_YYYY-MM-DD.png`).
- Check that iCloud Drive is enabled and synced.
- Verify automation permissions under **Settings > Shortcuts**.
- If running on macOS, allow the app in **Security & Privacy > Full Disk Access**.
- **macOS Unverified Developer Issue:**  
  If you see a warning message like "can’t check for malicious software" or "unverified developer", open **System Preferences > Security & Privacy > General** and click **"Allow Anyway"** to permit the app to run.

---

## Contributing 🤝

Feel free to contribute to this project by submitting issues, feature requests, or pull requests. Any improvements and suggestions are welcome!

---

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Cross-Platform Build Instructions

1. Install PyInstaller:
   $ pip install pyinstaller

2. In your project root (where CreateLockscreens.py is located), modify CreateLockscreens.py to run the "SetFile" command only on macOS:
   - Use an OS check (see next file for example).

3. Build the backend executable:
   On macOS:
     $ pyinstaller --onefile --console CreateLockscreens.py
   On Windows:
     $ pyinstaller --onefile --console CreateLockscreens.py

4. Verify in the "dist" folder you have:
   - macOS: "CreateLockscreens" (without extension)
   - Windows: "CreateLockscreens.exe"

5. Ensure both the GUI and backend executables are bundled together in your release.

## Steps to Build the Backend Executable:

1. Install PyInstaller if necessary:
   $ pip install pyinstaller

2. In the terminal, run:
   $ pyinstaller --onefile --console CreateLockscreens.py

3. Check the "dist" folder. You should see:
   dist/
      └── CreateLockscreens   (or CreateLockscreens.exe for Windows)

4. Ensure this executable is bundled with your GUI app. The GUI (custom_gui.py) should call the backend executable using its path.

5. Package both the GUI app and the CreateLockscreens executable in your release so users can run everything out-of-the-box.

Enjoy your countdown journey! 🎉

