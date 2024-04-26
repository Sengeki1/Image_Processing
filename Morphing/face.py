import numpy as np
import cv2 as cv
import dlib
from warp import triangulate

def crop_faces(image1_path, image2_path):
    cropped_faces_list = []
    for img in [image1_path, image2_path]:
        image = cv.imread(img)

        # convert to grayscale of each frames
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # read the haarcascade to detect the faces in an image
        face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # detects faces in the input image
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        print('Number of detected faces:', len(faces))

        # Crop and save each detected face
        cropped_faces = []
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cropped_faces.append(image[y: y + h, x:x + w])

        cropped_faces_list.append(cropped_faces)
    
    return cropped_faces_list

def generate_face_correspondeces(theImage1, theImage2):
    # Detect the points of face.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    imgList = crop_faces(theImage1, theImage2)
    list1 = []
    list2 = []
    feature_points = []
    cropped_images = []
    j = 1

    for m, img_list in enumerate(imgList):
        for img in img_list:

            if (j == 1):
                currList = list1
            else:
                currList = list2

            # Ask the detector to find the bounding boxes of each face. The 1 in the
            # second argument indicates that we should upsample the image 1 time. This
            # will make everything bigger and allow us to detect more faces.

            dets = detector(img, 1)

            try:
                if len(dets) == 0:
                    raise NoFaceFound  # type: ignore
            except NoFaceFound: # type: ignore
                print("Sorry, but I couldn't find a face in the image.")

            j = j + 1

            for k, rect in enumerate(dets):

                # Get landmarks/part for the face in rect
                shape = predictor(img, rect)
                
                for i in range(0, 68):
                    x = shape.part(i).x
                    y = shape.part(i).y
                    currList.append((x, y))
                    #cv.circle(img, (x, y), 1, (0, 255, 0), 2)
            
            feature_points.append(currList)
            cropped_images.append(img)

            cv.imwrite(f"test_{m}.png", img)


    return feature_points, cropped_images


img1 = './Images/mulher1.jpg'
img2 = './Images/homem.jpg'

feature_points, cropped_images = generate_face_correspondeces(img1, img2)

img_shape = []

for i, image in enumerate(cropped_images):
    #triangulate(image, feature_points[i])

    img_shape.append((image.shape[1], image.shape[0]))

src_pts = np.asarray(feature_points[1], dtype=np.float32)
dst_pts = np.asarray(feature_points[0], dtype=np.float32)

transformMatrix = cv.estimateAffine2D(src_pts, dst_pts)

warped_img = cv.warpAffine(cropped_images[1], transformMatrix[0], img_shape[0])

# Blending

alpha = 0.5  # Weight for the first image
beta = 1.0 - alpha  # Weight for the second image
blended_img = cv.addWeighted(warped_img, alpha, cropped_images[0], beta, 0)

cv.imshow("Blend", blended_img)
cv.waitKey(0)

