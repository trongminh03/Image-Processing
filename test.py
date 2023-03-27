import os
import cv2 
import sys
import numpy as np

# prefix = 'alternative_objects/obj_' + str(0) 
# obj_img = cv2.imread((prefix + str('.jpg'))) 
# dim = (46, 80)
# resized = cv2.resize(obj_img, dim, interpolation = cv2.INTER_AREA) 
# while True: 
#     cv2.imshow('Resized Image', resized)
#     cv2.waitKey(0)
#     sys.exit() # to exit from all the processes

MIN_ASPECT_RATIO = 0.1 
MAX_ASPECT_RATIO = 100
MIN_AREA = 200
MAX_AREA = 6000
MIN_AREA_DIFF = 0
MAX_AREA_DIFF = 20
box = []
original_dir = 'result_images/pokemon.jpg'
countours_list = []
img_ori = cv2.imread(original_dir, cv2.IMREAD_COLOR)
img = img_ori.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
img_canny = cv2.Canny(img_blur, 100, 200)
contours, _ = cv2.findContours(img_canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


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
            countours_list.append(cnt)

    if (aspect_ratio >= MIN_ASPECT_RATIO) and (aspect_ratio <= MAX_ASPECT_RATIO) and (rect_area >= MIN_AREA) and (rect_area <= MAX_AREA):
        # print(x, y, w, h)
        cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 1)

# black_img = np.zeros_like(img_ori) 
# cont = contours[1]
# cv2.drawContours(black_img, [cont], 0, (255, 255, 255), -1) 
# M = cv2.moments(cont)
# cx = int(M['m10'] / M['m00'])
# cy = int(M['m01'] / M['m00'])
# angle = 180
# rotation_matrix = cv2.getRotationMatrix2D((cx, cy), angle, 1) 
# rotated_contour = cv2.transform(cont.reshape(-1, 1, 2), rotation_matrix).reshape(-1, 2) 
# cv2.drawContours(black_img, [rotated_contour], 0, (255, 255, 255), cv2.FILLED)
# cv2.rectangle(img, (box[2][0], box[2][1]), (box[2][0] + box[2][2], box[2][1] + box[2][3]), (0, 255, 0), 1)
# opt=np.array(countours_list[2][1]).reshape(-1)
# print("list:", countours_list[2][1])
# print(opt)
# couple = []
# for i in countours_list[2][2]: 
#     couple.append(countours_list[2][2][0])
# # print("couple:", couple)
# b,g,r = (img_ori[couple[0][0], couple[0][1]])  

cont = countours_list[2] 
rect = box[2]
print("box:", box[2][1], box[2][0])
colord = (img_ori[box[2][1], box[2][0]])
b = int(colord[0])
g = int(colord[1])
r = int(colord[2])
print("b, g, r", b, g, r)
cv2.drawContours(img_ori, [cont], 0, (b, g, r), cv2.FILLED) 

# # cv2.drawContours(mask, [cont], -1, 0, -1) 
# # image = cv2.bitwise_and(img_ori, img_ori, mask=mask)
# # cv2.drawContours(image, [cont], 0, (b, g, r), -1) 

# print(cont)
M = cv2.moments(cont)
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])
angle = 180
rotation_matrix = cv2.getRotationMatrix2D((cx, cy), angle, 1) 
rotated_contour = cv2.transform(cont.reshape(-1, 1, 2), rotation_matrix).reshape(-1, 2) 

# cv2.drawContours(img_ori, [rotated_contour], 0, (169, 199, 123), cv2.FILLED)
cv2.drawContours(img_ori, [cont], 0, (b, g, r), cv2.FILLED) 
cv2.drawContours(img_ori, [rotated_contour], 0, (0, 0, 0), cv2.FILLED)
# print(b + g)
cv2.imshow('normal', img)
cv2.imshow('gray', img_gray)
cv2.imshow('black_img', img_ori) 
cv2.waitKey(0)
sys.exit() # to exit from all the processes
