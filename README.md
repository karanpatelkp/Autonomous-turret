
# Autonomous Turret System with Target Detection and Shooting

This project implements an **Autonomous Turret** that detects circular targets using computer vision and automatically aims and shoots gel bullets. It uses two degrees of freedom (pitch and yaw) with stepper motors controlled by a Raspberry Pi and an Adafruit Motor Hat.

## 🔧 Key Features

- 🎯 **Target Detection** using Hough Circle Transform (OpenCV)
- 🧠 **Raspberry Pi** for image processing and motor control
- ⚙️ **Stepper Motors** (Pitch & Yaw) controlled via Adafruit Motor HAT
- 🔁 **Pixel-to-Step Mapping**: Converts detected center in pixels to corresponding motor steps
- 🔫 **Relay-Controlled Firing Mechanism** to shoot gel bullets at the center of the target
- 🧪 **Presented at** the *Anoka Tech Fair Exhibition*, Amrita Vishwavidya Peetham, Coimbatore

## 🛠️ Hardware Used

- Raspberry Pi (any model with camera support)
- USB Camera / PiCamera
- 2x Stepper Motors
- Adafruit Motor HAT
- Relay Module
- Gel Gun Mechanism (or any safe firing device)
- Power Supply
- Jumper Wires

## 🧠 Software Stack

- Python 3
- OpenCV (`cv2`) for image processing
- `numpy` for matrix operations
- `adafruit_motorkit` for motor control
- `RPi.GPIO` for relay activation

## 🚀 How It Works

1. **Capture Video**: A live camera feed is opened.
2. **Detect Target**: Hough Circle Transform identifies circular targets in the frame.
3. **Calculate Center**: The pixel coordinates of the circle's center are mapped to stepper motor steps.
4. **Move Motors**:
   - Yaw control via `stepper2`
   - Pitch control via `stepper1`
5. **Fire Mechanism**:
   - Once aligned, a relay triggers the firing circuit to shoot a gel bullet.

## 📦 Setup & Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/karanpatelkp/Autonomous-Turret-system
   cd Autonomous-Turret-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Connect hardware** as per Raspberry Pi GPIO pin mappings.

4. **Run the script**
   ```bash
   python3 src/turret_main.py
   ```

## ⚠️ Safety Disclaimer

This project uses a firing mechanism. Ensure all safety precautions are taken during testing. Only use in controlled environments with non-harmful projectiles.

## 🧪 Future Improvements

- Add tracking for moving targets
- Auto-reset mechanism after firing
- Use of sensors for position feedback
- Improved GUI or web interface for manual override

## 📄 License

This project is open-sourced under the MIT License.

---

### 👨‍💻 Developed by Karan Patel  
Feel free to ⭐ the repository or contribute!  
GitHub: [Autonomous Turret System](https://github.com/karanpatelkp/Autonomous-Turret-system)
