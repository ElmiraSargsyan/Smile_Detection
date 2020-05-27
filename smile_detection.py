#with the function detect_smile() - difference of distances
import numpy as np
import imutils
import dlib
import cv2

from imutils.video import VideoStream
import datetime
import time

#_________________________________________________________________________

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

def detect_smile(mouth, nose, threshold = 0.1):
 
    #six points in the center of mouth
    center = np.concatenate((mouth[13:16], mouth[17:20]))
    CENTER_X = [x for (x, y) in center]
    CENTER_Y = [y for (x, y) in center]

    #two points of the edge of mouth
    edge = np.concatenate(([mouth[0]], [mouth[6]]))
    EDGE_X = [x for (x, y) in edge]
    EDGE_Y = [y for (x, y) in edge]
    
    mid = lambda arr: sum(arr)/len(arr)
    
    dist_center = np.linalg.norm(nose - (mid(CENTER_X), mid(CENTER_Y)))
    dist_edge = np.linalg.norm(nose - (mid(EDGE_X), mid(EDGE_Y)))
    
    return dist_center - dist_edge - threshold*dist_edge > 0

# Computes the EAR of the eye given by (x, y) coordinates and returns True if EAR is greater than given threshold
# V is vertical distance and H is horizontn al

def check_eye(eye, threshold = 0.2):

    V = np.linalg.norm(eye[1]-eye[5]) + np.linalg.norm(eye[2]-eye[4])
    H = np.linalg.norm(eye[0]-eye[3])

    EAR = V / (2.0 * H)
    
    return EAR > threshold


#_________________________________________________________________________

args = {"shape_predictor": "Pretrained_models/shape_predictor_68_face_landmarks.dat"}

landmark_indexes = {"mouth": (48, 68),
                    "right_eye": (36, 42),
                    "left_eye": (42, 48)}


#Initializing dlib's face detector and creating facial landmark predictor

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

#initializing video stream
print("*** Camera is turning on, please wait...")
vs = VideoStream().start()
print("*** Just a little bit more...")
time.sleep(2.0)


counter = 0  
smiling = False


# loop over the frames from the video stream
# detecting faces on the gray scaled image
# determining facial landmarks for the detected faces 
# checking if person is smiling and both eyes are open

while True:

    frame = vs.read()
    selfie = frame
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    
    for rect in rects:

        shape = predictor(gray, rect)
        shape = shape_to_np(shape)

        """
        # Drawing facial landmarks on the image
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        """
        
        (j, k) = landmark_indexes["mouth"]
        mouth = shape[j:k]
        (j, k) = landmark_indexes["right_eye"]
        right_eye = shape[j:k]
        (j, k) = landmark_indexes["left_eye"]
        left_eye = shape[j:k]
        
        """
        # Showing "True" on the image if the corresponding eye is opened
        cv2.putText(frame, str(check_eye(right_eye)), (x-50, y-100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(frame, str(check_eye(left_eye)), (x+50, y-100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        """
        
        if detect_smile(mouth, shape[33]) and check_eye(right_eye) and check_eye(left_eye):
            counter += 1
        else:
            counter = 0
            
        if counter > 15:
            smiling = True  
            
        """
            #Testing the smile detector on the image
            cv2.putText(frame, "smiling", (x+50, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.imshow("selfie", selfie)
        """    
                                    
            
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q") or smiling:
        break

# closing the windows and stopping videostreaming
cv2.destroyAllWindows()
vs.stop()

# Saving the captured selfie
if smiling:
    cv2.imwrite("captured_selfie.png", selfie) 
    print("*** Check the directory for captured image ^_^")


