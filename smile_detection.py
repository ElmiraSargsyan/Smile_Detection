#with the function detect_smile() - difference of distances

from imutils.video import VideoStream
import datetime
import time
import numpy as np
import argparse
import imutils
import dlib
import cv2
from imutils import face_utils

#Takes the rectangle predicted by dlib and converts it to the (x, y, width, height) format which is acceptable for OpenCV

def rect_to_bb(rect):

    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    return (x, y, w, h)


# Returns the numpy array of (x, y) coordinates of 68 facial landmarks

def shape_to_np(shape, dtype="int", l = 68):

    coords = np.zeros((l, 2), dtype=dtype)
    for i in range(l):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    return coords


# grab the (x, y)-coordinates associated with the face landmark
def visualize_facial_landmarks(image, shape, colors):

    output = image.copy()

    for key in landmark_indexes.keys():

        (j, k) = landmark_indexes[key]
        pts = shape[j:k]

        # compute the convex hull of the facial landmark coordinates points and display it
        hull = cv2.convexHull(pts)
        cv2.drawContours(output, [hull], -1, color = colors[key], thickness = -1)

    return output

#distance from the nose difference
# nose should be shape[33]

def detect_smile(mouth, nose):
 
    #6 points in the center of mouth
    center = np.concatenate((mouth[13:16], mouth[17:20]))
    CENTER_X = [x for (x, y) in center]
    CENTER_Y = [y for (x, y) in center]

    #two ponts of the edge of mouth
    edge = np.concatenate(([mouth[0]], [mouth[6]]))
    EDGE_X = [x for (x, y) in edge]
    EDGE_Y = [y for (x, y) in edge]
    
    mid = lambda arr: sum(arr)/len(arr)
    
    dist_center = np.linalg.norm(nose - (mid(CENTER_X), mid(CENTER_Y)))
    dist_edge = np.linalg.norm(nose - (mid(EDGE_X), mid(EDGE_Y)))
    
    return dist_center - dist_edge > 0

##!!!!! remove SmileDetection in the end

args = {"shape_predictor": "Pretrained_models/shape_predictor_68_face_landmarks.dat",
       "image": "SmileDetection/Images/negin.jpg"}

landmark_indexes = {"mouth": (48, 68),
                    "mouth_up": (61, 64),
                    "mouth_down": (65, 68),  
                    "right_eye": (36, 42),
                    "left_eye": (42, 48)}
landmark_colors = {"mouth": (19, 199, 109),
                    "right_eye": (168, 100, 168), 
                    "left_eye": (158, 163, 32)}

#Initializing dlib's face detector and creating facial landmark predictor

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

#initializing video stream
print("[INFO] camera is turning on, please wait...")
vs = VideoStream().start()
time.sleep(2.0)


# loop over the frames from the video stream
smile = 10
counter = 0
while True:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to grayscale
    frame = vs.read()
    selfie = frame
    #frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector(gray, 0)
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)


        # Drawing facial landmarks on the image
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        
        (j, k) = landmark_indexes["mouth"]
        mouth = shape[j:k]
        
        if detect_smile(mouth, shape[33]):
            counter += 1
        else:
            counter = 0
        if counter > 15:
            cv2.putText(frame, "smiling", (x+50, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.imshow("selfie", selfie)
            break
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

        
cv2.imshow("Selfie", selfie)

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()





