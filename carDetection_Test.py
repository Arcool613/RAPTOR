import cv2
import numpy as np

# Load the pre-trained MobileNet SSD model for object detection
net = cv2.dnn.readNetFromTensorflow('path/to/ssd_mobilenet_v1_coco/frozen_inference_graph.pb')

# Load class labels from coco.names file
with open('path/to/coco.names', 'r') as f:
    classes = f.read().strip().split('\n')

# Create VideoCapture objects for each camera
camera_1 = cv2.VideoCapture(0)  # Adjust the index based on your system
camera_2 = cv2.VideoCapture(1)  # Adjust the index based on your system
camera_3 = cv2.VideoCapture(2)  # Adjust the index based on your system
camera_4 = cv2.VideoCapture(3)  # Adjust the index based on your system

cameras = [camera_1, camera_2, camera_3, camera_4]

while True:
    frames = []
    
    # Read frames from all cameras
    for camera in cameras:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame")
            break
        frames.append(frame)

    # Resize and process frames for object detection
    for i, frame in enumerate(frames):
        height, width = frame.shape[:2]
        resized_frame = cv2.resize(frame, (300, 300))
        blob = cv2.dnn.blobFromImage(resized_frame, 0.007843, (300, 300), 127.5)

        # Set the input to the neural network
        net.setInput(blob)

        # Perform object detection
        detections = net.forward()

        # Loop over the detections
        for j in range(detections.shape[2]):
            confidence = detections[0, 0, j, 2]

            # If confidence is above a certain threshold (e.g., 0.5), consider it a detection
            if confidence > 0.5:
                class_id = int(detections[0, 0, j, 1])

                # Check if the detected object is a car
                if classes[class_id] == 'car':
                    box = detections[0, 0, j, 3:7] * np.array([width, height, width, height])
                    (startX, startY, endX, endY) = box.astype("int")

                    # Draw the bounding box around the detected car
                    cv2.rectangle(frames[i], (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Display the frames
    for i, frame in enumerate(frames):
        cv2.imshow(f"Camera {i+1}", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture objects
for camera in cameras:
    camera.release()

cv2.destroyAllWindows()
