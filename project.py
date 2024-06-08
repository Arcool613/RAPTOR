import cv2
try:    
    car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
except:
    print('Error')
finally:
    print('Done')
