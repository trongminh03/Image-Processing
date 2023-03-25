import cv2 
import numpy as np 

MIN_ASPECT_RATIO = 0.1 
MAX_ASPECT_RATIO = 100
MIN_AREA = 200
MAX_AREA = 6000
MIN_AREA_DIFF = 0
MAX_AREA_DIFF = 20
box = []
original_dir = 'result_images/pokemon.jpg'
contours_list = []
image = cv2.imread(original_dir, cv2.IMREAD_COLOR)
img = image.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
img_canny = cv2.Canny(img_blur, 100, 200)
contours, _ = cv2.findContours(img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for i in range(len(contours)):
    cnt = contours[i] 
    if i != len(contours) - 1:
        cnt2 = contours[i + 1]
        x2, y2, w2, h2 = cv2.boundingRect(cnt2)
        rect_area2 = w2 * h2  # area size
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = float(w) / h
    rect_area = w * h
    if (aspect_ratio >= MIN_ASPECT_RATIO) and (aspect_ratio <= MAX_ASPECT_RATIO) and (rect_area >= MIN_AREA) and (rect_area <= MAX_AREA):
        if (MIN_AREA_DIFF <= abs(rect_area - rect_area2)) and (abs(rect_area - rect_area2) <= MAX_AREA_DIFF):
            print("two if", x, y, w, h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            box.append(cv2.boundingRect(cnt))
            print("box", box[len(box) - 1])
            contours_list.append(cnt)

    if (aspect_ratio >= MIN_ASPECT_RATIO) and (aspect_ratio <= MAX_ASPECT_RATIO) and (rect_area >= MIN_AREA) and (rect_area <= MAX_AREA):
        print(x, y, w, h)
        cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 1)

print(len(contours))
cont = contours_list[2]
# Draw the contours on a white background
mask = np.ones(image.shape[:2], dtype="uint8") * 255
cv2.drawContours(mask, [cont], -1, (0, 0, 0), -1)

# Erase the contours from the original image
result = cv2.bitwise_and(image, image, mask=mask)

# Display the result
cv2.imshow('normal', image)
cv2.imshow('gray', img_gray)
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()