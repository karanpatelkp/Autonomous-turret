import cv2
import numpy as np
import time

# Import necessary libraries for motor control
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
import time

relay_pin = 17

GPIO.setmode(GPIO.BCM)



# Initialize the relay pin to HIGH to keep the relay off (since it's active LOW)
#GPIO.output(relay_pin, GPIO.LOW)

kit = MotorKit(i2c=board.I2C())

# Flag to control motor movement and loop
a = True

def detect_and_mark_circles(frame):
    # (Your circle detection code remains unchanged)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    # Detect circles using the Hough Circle Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=100, param2=40, minRadius=20, maxRadius=100)

    # Initialize x and y coordinates for the center
    x = 0
    y = 0

    # If circles are detected, process the first detected circle
    if circles is not None:
        circles = np.uint16(np.around(circles))
        i = circles[0][0]
        center = (i[0], i[1])
        radius = i[2]

        # Draw the detected circle and its center
        cv2.circle(frame, center, radius, (0, 255, 0), 2)
        cv2.circle(frame, center, 3, (0, 0, 255), 3)
        cv2.line(frame, (center[0] - 10, center[1]), (center[0] + 10, center[1]), (0, 0, 255), 2)
        cv2.line(frame, (center[0], center[1] - 10), (center[0], center[1] + 10), (0, 0, 255), 2)

        # Calculate x and y based on the center coordinates
        x = int(center[0] * 33 / 640)
        y = int(center[1] * 18 / 480)

    # Return the processed frame and coordinates
    return frame, x, y


if __name__ == "__main__":
    # Open a connection to the camera
    cap = cv2.VideoCapture(0)

    # Set the frame dimensions
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Height

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to capture frame.")
            break

        # Detect circles and get coordinates
        marked_frame, x, y = detect_and_mark_circles(frame)

        # Display the processed frame
        cv2.imshow("Detected Circles", marked_frame)

        # Print coordinates
        print(f"Center coordinates: ({x}, {y})")
        flag1, flag2=0, 0

        # Control steppers based on coordinates if circles are detected
        if x != 0 and y != 0:
            # Move stepper motors based on the x and y coordinates
            for i in range(x):
                kit.stepper2.onestep()  # Adjust this direction as needed
                time.sleep(0.1)
                flag1=1
            kit.stepper2.release()

            for i in range(y + 2):
                kit.stepper1.onestep(direction=stepper.BACKWARD)  # Adjust this direction as needed
                time.sleep(0.1)
                flag2=1
            kit.stepper1.release()
            
            if flag1 ==  1 and flag2 == 1:
                
                #time.sleep(0.5)  # Optional: delay to stabilize before firing
                #GPIO.output(relay_pin, GPIO.LOW)   # Activate relay (active LOW)
                #time.sleep(1.0)  # Gun is activated for 1 second
                #GPIO.output(relay_pin, GPIO.LOW)  # Deactivate relay
                GPIO.setup(relay_pin, GPIO.OUT)
                time.sleep(0.5)
                GPIO.cleanup()
            # Optionally exit the loop after firing
        break
        # Handle window closing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # Activate the gun after motor movements


        
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

    GPIO.cleanup()  # Clean up GPIO settings
