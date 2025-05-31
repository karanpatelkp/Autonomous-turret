# Importing necessary libraries for computer vision and time handling
import cv2
import numpy as np
import time

# Importing libraries for Raspberry Pi motor and GPIO control
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
# Defining GPIO pin connected to the relay module
relay_pin = 17

# Setting GPIO numbering mode to BCM (Broadcom SOC channel numbers)
GPIO.setmode(GPIO.BCM)

# Initializing motor driver (Adafruit Motor HAT) via I2C
kit = MotorKit(i2c=board.I2C())

# Defining a flag used later (currently unused)
a = True

# Defining function to detect circles in the camera frame and mark them
def detect_and_mark_circles(frame):
    # Converting frame to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Applying median blur to reduce noise
    gray = cv2.medianBlur(gray, 5)

    # Detecting circles using Hough Circle Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=100, param2=40, minRadius=20, maxRadius=100)

    # Initializing default center values
    x = 0
    y = 0

    # If a circle is detected
    if circles is not None:
        # Rounding off detected circle parameters to integer values
        circles = np.uint16(np.around(circles))
        i = circles[0][0]  # Taking the first detected circle

        center = (i[0], i[1])  # Getting the (x, y) center
        radius = i[2]          # Getting the radius

        # Drawing the outer circle
        cv2.circle(frame, center, radius, (0, 255, 0), 2)

        # Drawing the center of the circle
        cv2.circle(frame, center, 3, (0, 0, 255), 3)

        # Drawing crosshairs at the center
        cv2.line(frame, (center[0] - 10, center[1]), (center[0] + 10, center[1]), (0, 0, 255), 2)
        cv2.line(frame, (center[0], center[1] - 10), (center[0], center[1] + 10), (0, 0, 255), 2)

        # Converting pixel coordinates to stepper motor steps
        x = int(center[0] * 33 / 640)  # X axis has 33 steps for 640 pixels
        y = int(center[1] * 18 / 480)  # Y axis has 18 steps for 480 pixels

    # Returning modified frame and step values
    return frame, x, y


# Main function block
if __name__ == "__main__":
    # Opening video capture from default camera
    cap = cv2.VideoCapture(0)

    # Setting camera resolution to 640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Capturing one frame from the camera
        ret, frame = cap.read()

        # If reading the frame failed, exit
        if not ret:
            print("Failed to capture frame.")
            break

        # Detecting circles in the frame
        marked_frame, x, y = detect_and_mark_circles(frame)

        # Displaying the processed frame with detected circle
        cv2.imshow("Detected Circles", marked_frame)

        # Printing the calculated center in step units
        print(f"Center coordinates: ({x}, {y})")

        # Flags to check if motors moved
        flag1, flag2 = 0, 0

        # If a valid center is found
        if x != 0 and y != 0:
            # Moving yaw motor (stepper2) for x steps
            for i in range(x):
                kit.stepper2.onestep()  # Adjust direction if needed
                time.sleep(0.1)
                flag1 = 1
            kit.stepper2.release()  # Releasing the motor after moving

            # Moving pitch motor (stepper1) for y steps
            for i in range(y + 2):  # Added +2 for offset
                kit.stepper1.onestep(direction=stepper.BACKWARD)
                time.sleep(0.1)
                flag2 = 1
            kit.stepper1.release()  # Releasing the motor after moving
            
            # If both motors have moved, activating relay
            if flag1 == 1 and flag2 == 1:
                GPIO.setup(relay_pin, GPIO.OUT)  # Setting pin as output
                time.sleep(0.5)                  # Delay before firing
                GPIO.cleanup()                   # Cleaning up GPIOs

        # Exiting loop after one detection-shoot cycle
        break

        # Optionally allowing quitting by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Releasing the camera and closing all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Final cleanup of GPIOs
    GPIO.cleanup()
