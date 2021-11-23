import cv2
import numpy as np


import yaml
import tool_box


canvas = np.zeros([480, 640, 3], dtype=np.uint8)
canvas[:, :] = [255, 255, 255]


drawing = False
erase = True
ix, iy, radius = -1, -1, 5
blue, green, red = 0, 0, 0

def draw(event, x, y, flags, param):
	global ix, iy, drawing, radius, blue, green, red

	# To get the left mouse button
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		ix, iy = x, y

		if tool_box.CHOOSE_COLOR:
			tool_box.CHOOSE_COLOR = not tool_box.CHOOSE_COLOR 
			tool_box.color_palette()

		# To load the color
		with open('tools.yaml', 'r')  as file:
			blue, green, red = map(int, yaml.load(file, Loader=yaml.loader.BaseLoader)['color'])

	# To mouse move
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing:
			cv2.circle(canvas, (x, y), radius, (blue, green, red), -1)

		elif erase:
			cv2.circle(canvas, (x, y), radius, (255, 255, 255), -1)

	# To stop drawing
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False


cv2.namedWindow('Paint App')
cv2.setMouseCallback('Paint App', draw)

while True:
	cv2.imshow('Paint App', canvas)
	key = cv2.waitKey(1)

	if key == 27: break

	if key == ord('e'): erase = not erase
	if key == ord('c'): tool_box.CHOOSE_COLOR = not tool_box.CHOOSE_COLOR
	if key == ord('+') and radius <= 20: radius += 1
	if key == ord('-') and radius >= 2: radius -= 1

cv2.destroyAllWindows()