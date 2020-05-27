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


<p align="center">
<img src="Images/facial_landmarks_68markup.jpg" alt="facial landmarks" width="500" class="center"/> 
</p>

From the image, can be seen that facial regions can be accessed via simple Python indexing (the image above is one-indexed):

- The mouth can be accessed through points [48, 68].
- The right eye can be accessed through points [36, 42].
- The left eye can be accessed through points [42, 48].


____
### detecting smile

For smile detection I considered only the following 20 coordinates from facial landmarks.

<p align="center">
<img src="Images/mouth.png" alt="mouth landmarks" width="400" class="center"/> 
</p>

If the person is smiling the distance between 49 and 55 points increases, but that distance also will increase if person comes closer to the webcam.
besides the fact that the distance is increasing, the mentioned points move little bit up approaching to the nose.
Consequentely for detecting whether person is smiling or not I used the following key indicator. 


Let's suppose 
	`a1` is the midpoint of 49th and 55th landmark points
	`a2` is the midpoint of 6 mouth landmarks of the center of the mouth (62, 63, 64, 66, 67, 68)
	`n` is one of the points on the nose, particularly, I set n equal to the 34th point  
	
	
<p align="center">
<img src="Images/mouth_and_nose.jpg" alt="mouth and nose landmarks" width="500" class="center"/> 
</p>

if the ditance between `a1` and `n` is greater than the distance between `a2` and `b`, person is smiling.
in `detect_smile()` function threshold is added for higher accuracy



____

For checking the eyes are open or not I used Eye Aspect Ratio(EAR) from the ["Real-Time Eye Blink Detection using Facial Landmarks"](http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf) paper

 
![formula](https://render.githubusercontent.com/render/math?math=EAT=\frac{||p_2-p_6||%2B||p_3-p_5||}{2||p_1-p_4||})

<p align="center">
<img src="Images/EAR.jpg" alt="EAR visualization" width="400" class="center"/> 
</p>

If the eye is open EAT is relatively constant over time and is larger than when eye is closed, in this case EAT is more closer to zero.
