import numpy as np
import cv2 as cv
import dlib

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
    
    return cropped_faces



def generate_face_correspondeces(theImage1, theImage2):
    # Detect the points of face.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    corresp = np.zeros((68, 2))

    imgList = crop_faces(theImage1, theImage2)
    list1 = []
    list2 = []
    j = 1

    for img in imgList:

        size = (img.shape[0], img.shape[1])
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
                raise NoFaceFound # type: ignore
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
                corresp[i][0] += x
                corresp[i][1] += y




img1 = 'Images/mulher1.jpg'
img2 = 'Images/mulher2.jpeg'

generate_face_correspondeces(img1, img2)