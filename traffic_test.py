import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
# Set up GPIO pins for the green and red lights
GREEN_PIN = 21
RED_PIN = 26

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

reader = SimpleMFRC522()

try:
    id, text = reader.read()
    print("ID:", id)
    print("Text:", text)
    
    # Check if the tag ID is "12345678890"
    if str(id) in ["376956179222","577015848722"]:
        # Turn on the green light
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        print("Green light ON")
    else:
        # Turn on the red light
        GPIO.output(RED_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(RED_PIN, GPIO.LOW)
        print("Red light ON")

finally:
    GPIO.cleanup()