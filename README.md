# hynix_hindi_assistant
Offline Hindi voice assistant (privacy preserving) using RSP-5.
STEEPS
🛠 Hardware Requirements

RSP5 / Raspberry Pi 5 (or compatible Linux SBC)

Bluetooth Microphone

Bluetooth Speaker or Headphones

16GB or higher microSD card

Power adapter

Internet connection (for initial setup only)

 Software Requirements

Raspberry Pi OS (64-bit recommended)

Python 3.9 or higher

pip package manager

Bluetooth enabled

⚙ Initial Board Setup

Flash Raspberry Pi OS using Raspberry Pi Imager and boot the board.

Update system:

sudo apt update && sudo apt upgrade -y

Bluetooth Microphone & Speaker Setup

Enable Bluetooth:

sudo systemctl start bluetooth
sudo systemctl enable bluetooth
bluetoothctl


Inside bluetoothctl:

power on
scan on
pair XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
exit


(Replace XX with your device MAC address)

 Python Environment Setup

Install dependencies:

sudo apt install python3 python3-pip python3-venv portaudio19-dev -y


Create virtual environment:

python3 -m venv env
source env/bin/activate


Install project packages:

pip install -r requirements.txt

 Download Hindi Speech Model

Visit:

https://alphacephei.com/vosk/models

Download:

vosk-model-small-hi-0.22

Extract into:

models/

▶ Run Hindi Voice Assistant
python src/main.py

🎤 Test Microphone
python src/test_mic.py

Troubleshooting

Check mic devices:

arecord -l


Reconnect Bluetooth if audio drops

Lower sample rate if lag occurs
