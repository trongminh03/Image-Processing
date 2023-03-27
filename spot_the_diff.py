import cv2
import numpy as np
import imutils

# Load the two images
img1 = cv2.imread('result_images/pokemonAI.jpg')
img2 = cv2.imread("result_images/converted_image.jpg")

# img_height = img1.shape[0]

# Grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Find the difference between the two images
# Calculate absolute difference between two arrays 
diff = cv2.absdiff(gray1, gray2)
cv2.imshow("diff(img1, img2)", diff)

# Apply threshold. Apply both THRESH_BINARY and THRESH_OTSU
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("Threshold", thresh)

# Dilation
kernel = np.ones((5,5), np.uint8) 
dilate = cv2.dilate(thresh, kernel, iterations=2) 
cv2.imshow("Dilate", dilate)

# Calculate contours
contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

# Draw circles around the contours
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.circle(img2, (x + int(w/2), y + int(h/2)), int(np.sqrt((w/2)**2 + (h/2)**2)), (0, 0, 255), 2)

# Show the images with differences circled
cv2.imshow('Image 1 with differences circled', img1)
cv2.imshow('Image 2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()