import cv2
import pickle

# Load the pre-trained car detection model
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')  # Replace with the path to your cascade classifier XML file.

# Function to detect cars in an image
def detect_cars(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect cars in the image
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw rectangles around the detected cars
    for (x, y, w, h) in cars:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    return image, len(cars)

video = cv2.VideoCapture(0)

while True:
    ret,fram = video.read()
    if not ret:
        break
    
    frame_car , num_car = detect_cars(fram)
    cv2.imshow('Car Detection',frame_car)
    print(num_car)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
video.release()
cv2.destroyAllWindows()

