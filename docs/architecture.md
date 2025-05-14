
# System Architecture: Autonomous Turret System

This document outlines the high-level architecture and working flow of the Autonomous Turret System.

---

## 🔄 Overview

The system uses a Raspberry Pi to control two stepper motors (pitch and yaw) and a relay module for shooting. It detects a circular target in a video frame using OpenCV and computes the necessary motor steps to align the turret gun to the target's center before firing.

---

## 📐 System Components

### 1. **Camera (USB or PiCamera)**
- Captures live video stream (640x480 resolution).
- Sends frames to Raspberry Pi for processing.

### 2. **Raspberry Pi**
- Central controller for image processing, motor control, and shooting logic.
- Runs Python scripts with OpenCV and GPIO control libraries.

### 3. **Stepper Motors**
- 2 DOF (Degrees of Freedom):
  - **Stepper1** → Pitch control (Up/Down)
  - **Stepper2** → Yaw control (Left/Right)
- Controlled via **Adafruit Motor HAT** using the `adafruit_motorkit` library.

### 4. **Adafruit Motor HAT**
- Controls the two stepper motors using I2C.
- Connects directly to the Raspberry Pi.

### 5. **Relay Module**
- Controls the gel gun shooting circuit.
- Triggered when motors align the gun with the target's center.

---

## 🧠 Logic Flow

```text
[Camera Input]
      ↓
[Frame Capture by Raspberry Pi]
      ↓
[Grayscale Conversion + Median Blur]
      ↓
[Hough Circle Transform]
      ↓
[Target Center Detected (x, y in pixels)]
      ↓
[Pixel → Step Mapping]
      ↓
[Stepper Motor Movement (Yaw and Pitch)]
      ↓
[Alignment Check]
      ↓
[Relay Triggered → Gun Fires]
```

---

## ⚙️ Motor Control Logic

- Resolution conversion:
  - 640 pixels → X axis → ~33 motor steps
  - 480 pixels → Y axis → ~18 motor steps
- Compute `(x, y)` pixel position of target center
- Convert to `(step_x, step_y)`
- Move motors accordingly
- Fire when aligned

---

## 🧪 Exhibition

This system was demonstrated at the **Anoka Tech Fair Exhibition** held at *Amrita Vishwavidya Peetham, Coimbatore*.

---

## 🛡️ Notes

- Ensure proper power supply to motors and relay.
- Test with dummy load before using real gel bullets.
- Clean up GPIOs after execution.

