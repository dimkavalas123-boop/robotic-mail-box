📬 Robotic Mailbox (Raspberry Pi Zero W)

An interactive, physical smart mailbox created as a personal gift. Powered by a Raspberry Pi Zero W, this device receives text messages and photos in real-time via Telegram, physically notifies the user with mechanical movements and sound, and displays photos with custom animations on a TFT screen.

✨ Features

📩 Real-Time Telegram Integration: Receives messages and photos sent through a dedicated Telegram Bot and displays them on screen.

🦾 Physical Servo Mechanics:

Indicator Arm/Flag: Moves automatically when a new message arrives.

Internal Bell Ringer: A second servo motor physically strikes an internal bell to ring an audible alert.

🎨 Visual Effects & Animations: Real-time display animations built with Pygame that trigger alongside sound and physical alerts.

🗓️ Memory Calendar: An interactive photo gallery feature categorized by trips, seasons, and special moments with customized shuffle transition animations.

⚡ Optimized for Embedded Hardware: Utilizes pre-baked frame caching techniques to ensure smooth frame rates directly on the resource-constrained Raspberry Pi Zero W.

🛠️ Hardware Requirements

Microcontroller: Raspberry Pi Zero W

Display: SPI TFT Display Screen (/dev/fb1)

Actuators: 2x Micro Servo Motors (for flag movement and bell ringing)

Inputs: Physical Push Buttons connected via GPIO

Structure: Custom mailbox casing housing the Pi, display, servos, and physical bell.

💻 Tech Stack & Libraries

Language: Python 3

GUI & Graphics: pygame

Bot Framework: pyTelegramBotAPI (telebot)

Hardware Control: RPi.GPIO

Data Handling: pickle, json, multiprocessing

📁 Core Project Structure

.
├── main.py                   # Main entry point & application event loop
├── program_controler.py      # Core controller managing UI states & screens
├── get_telegram.py           # Background Telegram bot handler for incoming messages
├── animation_manager.py      # Manager for screen animations & pre-baked frame loader
├── bake_animations.py        # Utility script to pre-render/cache visual animations
├── ring_bell_func.py         # Servo motor controls for the physical bell ringer
├── buttons.py                # GPIO button detection and callback handlers
├── menu_class.py             # UI menu navigation for the photo calendar
└── update_screen.py          # Low-level screen buffer writer for the TFT display


🚀 Getting Started

Clone the Repository:

git clone https://github.com/dimkavalas123-boop/robotic-mail-box.git
cd robotic-mail-box


Install Dependencies:

pip install pygame pyTelegramBotAPI RPi.GPIO


Configure Environment Variables:
Set your Telegram Bot Token in your environment:

export TELEGRAM_TOKEN="YOUR_BOT_TOKEN_HERE"


Run the Application:

python3 main.py


💡 Notes on Embedded Performance

Running rich animations on a Raspberry Pi Zero W can be hardware-intensive. To achieve fluid performance without lag, non-essential heavy calculations and animation frames are pre-computed (baked) and cached locally, enabling effortless playback on the embedded screen.
