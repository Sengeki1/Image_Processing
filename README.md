# Image_Processing

Execute the following commands to install the required packages

* ```pip install cmake```
* ```pip install dlib```
* ```pip install opencv-python```
* ```pip install numpy```

## Morphing

Technique of morphing between two clips together was extended from morphing two still images

Input: Two images containing human faces (Image I₀ and Image I₁)

Output: A fluid transformation video transitioning from ```I₀``` to ```I₁```

We can look at the target transformation video results as a sequence of frames. Given two input images I₀ and I₁, at each timestamp t between ```0``` and ```1```, every pixel ```(x, y)``` in the morphed frame can be interpolated as follows:

$$M_t(x, y) = (1 - t) * I_0(x, y) + t * I_1(x, y)$$

When t equals 0, the morphed frame is exactly the Image I₀, when t equals 1, the morphed frame is exactly the Image I₁, and frame at t is the blending of two images at time t. This is called “cross-dissolve” in the film industry. Cross dissolve handles the photometric side of the problem, it balances out the coloration in the middle frames, but will inevitably leave the “ghosting” effects if the two faces aren’t perfectly aligned. 

![alt text](/Images/image.png)
<p align="center">Left: Image I₀, Middle: Image I₁, Right: Cross-dissolve of two images</p>

to align the shape in between the output, we need to make sure that the important features can be consistently matched throughout the frames. If the point pairs were given, we can then calculate the new location of corresponding points in each morphed frames to create the average warped shape.

Now, we have a high-level idea of how morphing frames are calculated.

Given the corresponding features pairs, for each frame at time t:

1. Compute the intermediate shape by linear interpolation of each feature pair

$$x_t = (1 - t) * x_i + t * x_j$$

$$y_t = (1 - t) * y_i + t * y_j$$

2. Cross dissolve the color by interpolating two images

$$M(x_t, y_t) = (1 - t) * I_0(x_i, y_i) + t * I_1(x_j, y_j)$$


### Detecting facial landmarks

In the algorithm above, we assume, the input correspondences at key feature points were given. A brute force way is to manually select correspondences, which is time-consuming and prone to human errors. Thus, we will need to find a way to smartly select important facial features correspondences.

Here we will utilize dlib to detect facial landmarks. Facial landmarks are used to localize the face in the image and detect the key facial structures on the face. 

The facial landmark detector will give us the estimated location of 68 (x, y) pair coordinates that represent salient regions of the face, including eye, eyebrows, nose, mouth, and jawline.

![alt text](/Images/image-1.png)

<p align="center">68 points selection on Image 0 and Image 1 from dlib’s facial landmarks</p>

In addition to the 68 facial feature points, we also need to select some points outside of the face to include the background into the morphing frames. To make sure the background is included, we need to select at least 4 points (4 corners), here we will use 8 points (4 corners + 4 center points from each edge) to make the transition more smooth.

For more explanation <https://azmariewang.medium.com/face-morphing-a-step-by-step-tutorial-with-code-75a663cdc666>
