import numpy as np
import cv2

cv2.namedWindow('Saver')
cap = cv2.VideoCapture('video.mp4')
ret, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
cv2.imshow('Saver', frame)
cv2.imwrite('frame.png',frame)
