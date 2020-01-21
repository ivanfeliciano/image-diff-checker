import numpy as np
import cv2

REF_POINTS = []
def click_roi(event, x, y, flags, param):
	global REF_POINTS
	if event == cv2.EVENT_LBUTTONDOWN:
		REF_POINTS.append((x, y))
	elif event == cv2.EVENT_LBUTTONUP:
		REF_POINTS.append((x, y))
 
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)
cv2.setMouseCallback('frame', click_roi)
ret, prev_frame = cap.read()

current_roi = []
prev_roi = []
while(True):
	ret, frame = cap.read()
	image_to_show = frame.copy()
	coord_rois = []
	for i in range(0, len(REF_POINTS), 2):
		if i + 1 < len(REF_POINTS):
			coord_rois.append((REF_POINTS[i], REF_POINTS[i + 1]))
			cv2.rectangle(image_to_show, REF_POINTS[i], REF_POINTS[i + 1], (255, 0, 0), 2)
	current_roi = []
	for coordinates in coord_rois:
		roi = image_to_show[coordinates[0][1]:coordinates[1][1],\
				coordinates[0][0]:coordinates[1][0]]
		current_roi.append(roi)
	for roi_idx in range(len(prev_roi)):
		difference = cv2.subtract(prev_roi[roi_idx], current_roi[roi_idx])
		difference = cv2.cvtColor(difference, cv2.COLOR_RGB2GRAY)
		ret, thresh = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY_INV)
		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			x,y,w,h = cv2.boundingRect(cnt)
			cv2.rectangle(image_to_show, (coord_rois[roi_idx][0][0] + x, coord_rois[roi_idx][0][1] + y),\
						(coord_rois[roi_idx][0][0] + x + w, coord_rois[roi_idx][0][1] + y + h), (0, 0, 255), 2)
	prev_roi = current_roi.copy()
	cv2.imshow('frame', image_to_show)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
