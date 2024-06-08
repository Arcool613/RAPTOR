import cv2
import numpy as np
import time

def initialize_cameras(camera_indices):
    caps = []
    frames = []

    for index in camera_indices:
        cap = cv2.VideoCapture(index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        caps.append(cap)
        frames.append(None)

    return caps, frames

def detect_cars(frame, algo, min_width, min_height, offset, count_line_pos, line_thickness):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 5)

    img_sub = algo.apply(blur)
    dil = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dil_2 = cv2.morphologyEx(dil, cv2.MORPH_CLOSE, kernel)
    dil_2 = cv2.morphologyEx(dil_2, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(dil_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (0, count_line_pos), (frame.shape[1], count_line_pos), (0, 255, 0), line_thickness)

    detected_cars = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        validate_counter = (w >= min_width) and (h >= min_height)

        if validate_counter:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = (x + w // 2, y + h // 2)
            detected_cars.append(center)
            cv2.circle(frame, center, 4, (0, 0, 255), -1)

    return frame, detected_cars

def count_cars(caps, frames, algo, min_width, min_height, offset, count_line_pos, line_thickness, duration):
    num_cameras = len(caps)
    counter = [0] * num_cameras
    detect = [[] for _ in range(num_cameras)]
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        for i in range(num_cameras):
            ret, frame = caps[i].read()
            if not ret:
                break
            frames[i] = frame

        for i in range(num_cameras):
            frame = frames[i]
            frame, detected_cars = detect_cars(frame, algo, min_width, min_height, offset, count_line_pos, line_thickness)

            for center in detected_cars:
                if (count_line_pos + offset) > center[1] > (count_line_pos - offset):
                    counter[i] += 1
                    print(f'Camera {i + 1} - Vehicle Counter: {counter[i]}')

            cv2.line(frame, (0, count_line_pos), (frame.shape[1], count_line_pos), (0, 0, 255), line_thickness)

            cv2.imshow(f'Lane {i + 1}', frame)

        if cv2.waitKey(1) == 27 & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    for cap in caps:
        cap.release()

    return counter

def traffic_count(camera_indices, duration):
    caps, frames = initialize_cameras(camera_indices)

    count_line_pos = 300
    line_thickness = 2
    min_width = 80
    min_height = 80
    algo = cv2.createBackgroundSubtractorMOG2()
    offset = 6

    counter = count_cars(caps, frames, algo, min_width, min_height, offset, count_line_pos, line_thickness, duration)
    
    return counter

def main_func():
    # Define camera indices (modify as needed)
    camera_indices = [6,4]
    camera_indices = [0]
    # Define the duration for car counting (in seconds)
    duration = 60

    # Call the traffic_count function
    car_counts = traffic_count(camera_indices, duration)

    # Print the car counts for each camera
    for i, count in enumerate(car_counts):
        print(f'Camera {i + 1} - Vehicle Count: {count}')

    # Define camera indices (modify as needed)
    camera_indice = [2,0]

    # Define the duration for car counting (in seconds)
    durations = 20
        
        
    # Call the traffic_count function
    car_counts = traffic_count(camera_indice, durations)

    # Print the car counts for each camera
    for i, count in enumerate(car_counts):
        print(f'Camera {i + 3} - Vehicle Count: {count}')
main_func()