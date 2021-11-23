import cv2

video = cv2.VideoCapture(0)
fist_cascade = cv2.CascadeClassifier('fist.xml')
palm_cascade = cv2.CascadeClassifier('palm.xml')

def object_detection(draw, image, cascade, scaleFactor=1.2, minNeighbors=5):
	objects = cascade.detectMultiScale(image, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

	for obj in objects:
		x, y, w, h = obj
		cv2.rectangle(draw, (x, y), (x+w, y+h), (0, 255, 0), 3) 
	return draw

while True:
	_, frame = video.read()

	gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	image = object_detection(frame, gray_scale, fist_cascade)
	image = object_detection(image, gray_scale, palm_cascade)

	cv2.imshow('Capturing', image)

	key = cv2.waitKey(1)

	if key == 27: break

video.release()
cv2.destroyAllWindows()