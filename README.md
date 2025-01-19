## Countdown Lockscreen Setup Guide

Welcome to the Countdown Lockscreen project! This guide will walk you through setting up your environment, generating lock screen images, and automating their updates to your iPhone.

### Prerequisites ✅
- Python 3 installed
- Virtual environment (`venv`) setup
- Git installed
- iCloud Drive enabled on your Mac/iPhone

---

### Steps to Set Up the Project ⚙️

#### 1. Clone the Repository 🛠️
```bash
git clone https://github.com/yourusername/countdown-lockscreen.git
cd countdown-lockscreen
```

#### 2. Set Up the Virtual Environment 🐍
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

#### 3. Install Dependencies 📦
```bash
pip install -r requirements.txt
```

#### 4. Generate Countdown Images 🖼️
```bash
python CreateLockscreens.py
```
This will generate all lock screen images and save them as a ZIP file named `countdown_photos.zip`.

#### 5. Upload to iCloud 📤
1. Unzip `countdown_photos.zip`.
2. Move the extracted folder to `iCloud Drive > Shortcuts`.

#### 6. Create iOS Shortcut ⚡
1. Open the **Shortcuts** app on your iPhone.
2. Create a new automation:
   - **Trigger:** `Time of Day` (e.g., Midnight)
   - **Action:** `Find Photos in iCloud` > `Set Wallpaper`
3. Select the countdown folder and configure it to update your lock screen daily.

#### 7. Enjoy Your Dynamic Lock Screen 🎉
Now, your iPhone will update the lock screen every day with the countdown image!

---

### Contributing 🤝
If you want to improve this project, feel free to fork it, submit pull requests, and share feedback!

---

### License 📄
This project is licensed under the MIT License.
