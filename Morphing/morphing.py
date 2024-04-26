import cv2

# Load the two images
image1 = cv2.imread('Images/mulher1.jpg')
image2 = cv2.imread('Images/mulher2.jpeg')

# Convert images to grayscale
image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Initialize the SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors for both images
keypoints1, descriptors1 = sift.detectAndCompute(image1_gray, None)
keypoints2, descriptors2 = sift.detectAndCompute(image2_gray, None)

# Initialize a brute-force matcher
bf = cv2.BFMatcher()

# Match descriptors between the two images
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# Apply ratio test to filter good matches
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# Draw matched keypoints
matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the matched keypoints
cv2.imshow('Matched Keypoints', matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
