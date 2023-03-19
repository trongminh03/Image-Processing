import os
import cv2 
import sys

box = []
original_dir = 'result_images/original_image.jpg'
img_ori = cv2.imread(original_dir, cv2.IMREAD_COLOR)
img = img_ori.copy()
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
    if (aspect_ratio >= 0.1) and (aspect_ratio <= 10000.0) and (rect_area >= 500) and (rect_area <= 10000):
        if (0 <= abs(rect_area - rect_area2)) and (abs(rect_area - rect_area2) <= 20):
            print("two if", x, y, w, h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            box.append(cv2.boundingRect(cnt))
            print("box", box[len(box) - 1])

    # if (aspect_ratio >= 0.1) and (aspect_ratio <= 1000) and (rect_area >= 500) and (rect_area <= 10000):
    #     print(x, y, w, h)
    #     cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 1)

while True: 
    cv2.imshow('normal', img)
    cv2.imshow('gray', img_gray)
    cv2.waitKey(0)
    sys.exit() # to exit from all the processes
 
# cv2.destroyAllWindows() # destroy all windows
