import cv2
import numpy as np


import yaml
import tool_box


canvas = np.zeros([480, 640, 3], dtype=np.uint8)
canvas[:, :] = [255, 255, 255]

erase = False

video = cv2.VideoCapture(0)
fist_cascade = cv2.CascadeClassifier('fist.xml')

def image_detection(draw, image, cascade_classifier, scale=1.2, neighbors=5):
	objects = cascade_classifier.detectMultiScale(image, scaleFactor=scale, minNeighbors=neighbors)

	for object in objects:
		x, y, w, h = object
		cv2.rectangle(draw, (x, y), (x+w, y+h), (0, 255, 0), 2)

def detect_motion(image, cascade_classifier, scale=1.2, neighbors=5):
	objects = cascade_classifier.detectMultiScale(image, scaleFactor=scale, minNeighbors=neighbors)
	if len(objects):
		x, y, w, h = objects[0]
		radius = 10
		area_factor = (w * h) / (640*480)
		print(area_factor)
		if 0.1 <= area_factor <= 0.18:
			radius = 20
		elif 0.08 <= area_factor < 0.1:
			radius = 15

		return (x + w //2, y + h // 2, radius)
	else:
		return (-1, -1, 0)

def touchless_paint(image, x, y, r):
	if tool_box.CHOOSE_COLOR:
		tool_box.color_palette()
		tool_box.CHOOSE_COLOR = False

	with open('tools.yaml', 'r') as file:
		dictionary = yaml.load(file, Loader=yaml.loader.BaseLoader)
		if dictionary:
			red, blue, green = map(int, dictionary['color'])
		else:
			blue, green, red = 0, 0, 0
	if not erase: 
		cv2.circle(image, (x, y), r, (blue, green, red), -1)

	else:
		cv2.circle(image, (x, y), r, (255, 255, 255), -1)

while True:
	_ , frame = video.read()
	gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	x_c, y_c, r = detect_motion(gray_scale, fist_cascade)
	touchless_paint(canvas, x_c, y_c, r)
	
	cv2.imshow('Paint App', cv2.flip(canvas, 180))
	key = cv2.waitKey(1)

	if key == 27: break

	if key == ord('e'): erase = not erase
	if key == ord('c'): tool_box.CHOOSE_COLOR = not tool_box.CHOOSE_COLOR
	
cv2.destroyAllWindows()
