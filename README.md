# SmileDetection
The script turns on the web cam, detects the human face and automatically takes a picture when the person is smiling and his/her both eyes are open. 

Dlib is not compatible with python 3.7
 none of the .whl file were compatible with 3.7
 
 
 
 
 
Step #1: Localize the face in the image.
Step #2: Detect the key facial structures on the face ROI.
	Mouth
	Right eyebrow
	Left eyebrow
	Right eye
	Left eye
	Nose
	Jaw

The facial landmark detector included in the dlib library  which uses pretrained regression trees

https://www.pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup-768x619.jpg