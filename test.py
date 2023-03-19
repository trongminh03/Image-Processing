import os
import cv2 
import sys

MIN_ASPECT_RATIO = 0.1 
MAX_ASPECT_RATIO = 100
MIN_AREA = 200 
MAX_AREA = 2000
MIN_AREA_DIFF = 0
MAX_AREA_DIFF = 20
# box = []
# original_dir = 'result_images/CN pic.jpg'
# img_ori = cv2.imread(original_dir, cv2.IMREAD_COLOR)
# img = img_ori.copy()
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
# img_canny = cv2.Canny(img_blur, 100, 200)
# contours, _ = cv2.findContours(img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

prefix = 'alternative_objects/obj_' + str(0) 
obj_img = cv2.imread((prefix + str('.jpg'))) 
dim = (46, 80)
resized = cv2.resize(obj_img, dim, interpolation = cv2.INTER_AREA) 
while True: 
    cv2.imshow('Resized Image', resized)
    cv2.waitKey(0)
    sys.exit() # to exit from all the processes



# for i in range(len(contours)):
#     cnt = contours[i] 
#     if i != len(contours) - 1:
#         cnt2 = contours[i + 1]
#         x2, y2, w2, h2 = cv2.boundingRect(cnt2)
#         rect_area2 = w2 * h2  # area size
#     x, y, w, h = cv2.boundingRect(cnt)
#     aspect_ratio = float(w) / h
#     rect_area = w * h
#     if (aspect_ratio >= 0.1) and (aspect_ratio <= 100) and (rect_area >= 200) and (rect_area <= 5000):
#         if (0 <= abs(rect_area - rect_area2)) and (abs(rect_area - rect_area2) <= 20):
#             print("two if", x, y, w, h)
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
#             box.append(cv2.boundingRect(cnt))
#             print("box", box[len(box) - 1])

#     if (aspect_ratio >= MIN_ASPECT_RATIO) and (aspect_ratio <= MAX_ASPECT_RATIO) and (rect_area >= MIN_AREA) and (rect_area <= MAX_AREA):
#         print(x, y, w, h)
#         cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 1)

# while True: 
#     cv2.imshow('normal', img)
#     cv2.imshow('gray', img_gray)
#     cv2.waitKey(0)
#     sys.exit() # to exit from all the processes
 
cv2.destroyAllWindows() # destroy all windows
