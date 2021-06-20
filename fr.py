# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition 
import argparse
import imutils
import pickle
import numpy
import pkg_resources
import time
from cv2 import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", default = "haarcascade_frontalface_default.xml" ,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", default = "encodings.pickle",
	help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

haar_xml = pkg_resources.resource_filename(
    'cv2', 'data/haarcascade_frontalface_default.xml')

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(haar_xml)
# initialize the video stream and allow the camera sensor to warm up


vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 0


while True:
    frame = vs.read()
    
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame.png"
        cv2.imwrite(img_name, frame)
        print("{}written!".format(img_name))
        break

frame = imutils.resize(frame, width=500)
	
# convert the input frame from (1) BGR to grayscale (for face
# detection) and (2) from BGR to RGB (for face recognition)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# detect faces in the grayscale frame
rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
	minNeighbors=5, minSize=(30, 30))
	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we
	# need to do a bit of reordering
boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
	# compute the facial embeddings for each face bounding box
encodings = face_recognition.face_encodings(rgb, boxes)

# loop over the facial embeddings
for encoding in encodings:
	# attempt to match each face in the input image to our known
	# encodings
	face_distances = face_recognition.face_distance(data["encodings"], encoding)
	print(face_distances)
	ind = numpy.argmin(face_distances)
	print(ind)
	matches = face_recognition.compare_faces(data["encodings"],
		encoding)
	name = "Unknown"
	# check to see if we have found a match
	if (True in matches) :
		name = data["names"][ind]

print(name)
cv2.destroyAllWindows()
vs.stop()
