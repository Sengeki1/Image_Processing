import cv2 as cv

img1 = cv.imread('./Images/1.webp')
img2 = cv.imread('./Images/bunny.jpg')

roi = img1[0:img2.shape[0], 0:img2.shape[1]]

# Theoretical sum
f_roi = cv.bitwise_and(roi, img2)

cv.imshow('result', f_roi)
cv.waitKey(0)