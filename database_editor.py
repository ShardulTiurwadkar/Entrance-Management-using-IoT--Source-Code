# USAGE
# python build_face_dataset.py --cascade haarcascade_frontalface_default.xml --output dataset/adrian

# import the necessary packages
from imutils.video import VideoStream
import argparse
import shutil
import imutils
import time
from cv2 import cv2
import os
import pkg_resources
haar_xml = pkg_resources.resource_filename(
    'cv2', '/home/pi/.local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default = "dataset",
	help="path to output directory")
args = vars(ap.parse_args())
# load OpenCV's Haar cascade for face detection from disk
detector = cv2.CascadeClassifier("/home/pi/.local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml")

s = input("Enter 'A' TO ADD NEW ENTRY / UPDATE THE ENTRY  OR 'D' TO DELETE THE ENTRY: ")
identity = input("ENTER THE NAME: ")
if  (s == 'A') :

	
	if not os.path.exists(args["output"]+"/"+identity):
		os.makedirs(args["output"]+"/"+identity)
		print("new directory "+ identity + " created")
	else:
		print("directory" + identity + " exists in the database.")
	# initialize the video stream, allow the camera sensor to warm up,
	# and initialize the total number of example faces written to disk
	# thus far
	print("[INFO] starting video stream...")
	#vs = VideoStream(src=0).start()
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)
	list = os.listdir(args["output"]+"/"+identity) # dir is your directory path
	total = len(list)

	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream, clone it, (just
		# in case we want to write it to disk), and then resize the frame
		# so we can apply face detection faster
		frame = vs.read()
		orig = frame.copy()
		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# detect faces in the grayscale frame
		rects = detector.detectMultiScale(
			gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

		# loop over the face detections and draw them on the frame
		for (x, y, w, h) in rects:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the spacebar was pressed, write the *original* frame to disk
		# so we can later process it and use it for face recognition
		if key % 256 == 32:
			p = os.path.sep.join([args["output"]+"/"+identity, "{}.png".format(
				str(total).zfill(5))])
			print("pic taken")
			cv2.imwrite(p, orig)
			total += 1

		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break

	# do a bit of cleanup
	print("[INFO] {} face images stored".format(total))
	print("[INFO] cleaning up...")
	cv2.destroyAllWindows()
	vs.stop()
	os.system("python encoderr.py")

elif s == 'D':
	if os.path.exists(args["output"]+"/"+identity):
		shutil.rmtree(args["output"]+"/"+identity)
	print("directory " + identity + " deleted")
	if not os.listdir(args["output"]):
		os.remove("encodings.pickle")
	else:
		os.system("python encoderr.py")
else :
	print("false input")