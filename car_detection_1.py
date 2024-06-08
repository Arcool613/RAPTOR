import cv2
import time

# Load the Haar Cascade classifier for car detection
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')  # Replace with the actual path

# Open the video capture object (camera index 0)
cap = cv2.VideoCapture(0)

# Function to perform car detection
def detect_cars(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect cars in the frame
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

# Main loop
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame")
        break

    # Perform car detection on the frame
    frame_with_cars = detect_cars(frame)

    # Display the frame with detected cars
    cv2.imshow('Car Detection', frame_with_cars)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
