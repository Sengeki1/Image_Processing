import numpy as np
import cv2 as cv

def triangulate(image, points):

    # Create Subdiv2D object
    rect = (0, 0, image.shape[0], image.shape[1])  # Rectangle covering the entire image
    triangulation = cv.Subdiv2D(rect)

      # Insert points into triangulation object
    valid_points = []  # List to store valid points within the image bounds
    for point in points:
        x, y = point
        if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:  # Check if point is within image bounds
            triangulation.insert((x, y))
            valid_points.append((x, y))
        
    # Get triangles
    triangleList1 = triangulation.getTriangleList()

    # Draw triangles on the image (optional)
    for t in triangleList1:
        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))
        cv.line(image, pt1, pt2, (0, 255, 0), 1, cv.LINE_AA)
        cv.line(image, pt2, pt3, (0, 255, 0), 1, cv.LINE_AA)
        cv.line(image, pt3, pt1, (0, 255, 0), 1, cv.LINE_AA)

    # Show or return the triangulated image (optional)
    cv.imshow('Triangulated Image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()
