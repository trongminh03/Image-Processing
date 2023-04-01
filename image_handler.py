import cv2
import os
import random
import numpy as np
from image_generator import imageGeneratorOpenAI

class convertImageMaker: 
    MIN_ASPECT_RATIO = 0.1 
    MAX_ASPECT_RATIO = 100
    MIN_AREA = 300 
    MAX_AREA = 5000
    MIN_AREA_DIFF = 0
    MAX_AREA_DIFF = 20
    MAX_REPLACEMENT = 4
    MAX_DIFFERENCE = 20

    def __init__(self):
        self.box = []
        self.contours = []
        self.abs_dir = "./result_images"
        self.crop_location = str()
        self.crop_cnt = 0
        self.convert_type = int()
        self.original_dir = ""
        self.alternative_obj_index = 0
        self.diff_count = 0
        self.imageGenerator = imageGeneratorOpenAI()
        pass

    def image_extract(self, img_name='original_image'): 
        original_dir = 'result_images/' + img_name + '.jpg'
        self.original_dir=original_dir
        print(original_dir)
        img_ori = cv2.imread(original_dir, cv2.IMREAD_COLOR)
        # print(img_ori)
        img = img_ori.copy()
        #convert img to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #apply Gaussian Blur to grayscale img to smooth out any noise and makes it easier to identify edges
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
        #apply canny to blurred img to identify the edges of objects in the image
        img_canny = cv2.Canny(img_blur, 100, 200)
        contours, _ = cv2.findContours(img_canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   

        for i in range(len(contours)):
            cnt = contours[i]
            if i != len(contours) - 1:
                cnt2 = contours[i + 1]
                x2, y2, w2, h2 = cv2.boundingRect(cnt2)
                rect_area2 = w2 * h2  # area size
            x, y, w, h = cv2.boundingRect(cnt)
            rect_area = w * h  # area size
            aspect_ratio = float(w) / h  # ratio = width/height
            if (aspect_ratio >= self.MIN_ASPECT_RATIO) and (aspect_ratio <= self.MAX_ASPECT_RATIO) and (rect_area >= self.MIN_AREA) and (rect_area <= self.MAX_AREA):
                if (self.MIN_AREA_DIFF <= abs(rect_area - rect_area2)) and (abs(rect_area - rect_area2) <= self.MAX_AREA_DIFF):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    self.box.append(cv2.boundingRect(cnt))
                    print(str(self.box[len(self.box) - 1][3]) + " " + str(self.box[len(self.box) - 1][2]))
                    self.contours.append(cnt)
                    # print(cnt)

        #sort according to x
        for i in range(len(self.box)):  # Buble Sort on python
            for j in range(len(self.box) - (i + 1)):
                if self.box[j][0] > self.box[j + 1][0]:
                    temp = self.box[j]
                    self.box[j] = self.box[j + 1]
                    self.box[j + 1] = temp
                    tmp = self.contours[j] 
                    self.contours[j] = self.contours[j + 1] 
                    self.contours[j + 1] = tmp  
                    pass
                pass
            pass
    
    def crop_image(self, item_index): 
        crop_list = []
        crop_dir = 'crop_images'
        img_ori = cv2.imread(self.original_dir, cv2.IMREAD_COLOR) 
        img_cut = img_ori.copy()
        img_cut2 = img_ori.copy()
        crop_text = open(os.path.join(crop_dir, "crop_location.txt"), 'w')
        crop_img = img_ori[self.box[item_index][1]:self.box[item_index][1] + self.box[item_index][3], self.box[item_index][0]:self.box[item_index][0]+self.box[item_index][2]]
        #data in crop_location y, h, x, w
        data = str(self.box[item_index][1]) + " " + str(self.box[item_index][3]) + " " + str(self.box[item_index][0]) + " " + str(self.box[item_index][2]) + "\n"
        crop_text.write(data)
        crop_list.append(crop_img)
        print(crop_dir, "crop_" + str(item_index) + ".jpg")
        cv2.imwrite(os.path.join(crop_dir, "crop_" + str(item_index) + ".jpg"), crop_img)
        img_cut[self.box[item_index][1]:self.box[item_index][1] + self.box[item_index][3], self.box[item_index][0]:self.box[item_index][0] + self.box[item_index][2]] = 0
        img_cut2[self.box[item_index][1]:self.box[item_index][1] + self.box[item_index][3], self.box[item_index][0]:self.box[item_index][0] + self.box[item_index][2]] = 255
        cv2.imwrite(os.path.join(crop_dir, "cut_image1.jpg"), img_cut)
        cv2.imwrite(os.path.join(crop_dir, "cut_image2.jpg"), img_cut2)
        self.crop_cnt += 1
        pass
    
    #rearrange this one 
    def image_convert(self, convert_type): 
        img_ori = cv2.imread(self.original_dir, cv2.IMREAD_COLOR) 
        for item_index in range(len(self.box)): 
            if self.diff_count == self.MAX_DIFFERENCE: 
                break
            self.diff_count += 1
            if convert_type == 1: 
                self.change_color_image(img_ori, item_index) 
                pass 
            elif convert_type == 2 and self.alternative_obj_index != self.MAX_REPLACEMENT: 
                self.replace_with_another_object(img_ori, item_index)
                pass 
            elif convert_type == 3: 
                self.change_color_image_advanced(img_ori, item_index)
                pass 
            elif convert_type == 4: 
                self.flip_image(img_ori, item_index)
                pass 
            elif convert_type == 5: 
                self.blend_with_background_color(img_ori, item_index)
                pass
            elif convert_type == 6: 
                self.flip_image_advanced(img_ori, item_index)
                pass
            elif self.alternative_obj_index == self.MAX_REPLACEMENT: 
                pass
        cv2.imwrite(os.path.join("result_images/converted_image.jpg"), img_ori)
        pass     

    def image_convert_mix(self): 
        img_ori = cv2.imread(self.original_dir, cv2.IMREAD_COLOR)
        print("box length", len(self.box))
        for item_index in range(len(self.box)): 
            if self.diff_count == self.MAX_DIFFERENCE: 
                break
            self.diff_count += 1
            if self.alternative_obj_index != self.MAX_REPLACEMENT: 
                convert_type = random.randint(1, 6)
            else: 
                convert_type = random.choice([1, 3, 4, 5, 6])
            if convert_type == 1: 
                self.change_color_image(img_ori, item_index) 
            elif convert_type == 2 and self.alternative_obj_index != self.MAX_REPLACEMENT: 
                self.replace_with_another_object(img_ori, item_index) 
            elif convert_type == 3: 
                self.change_color_image_advanced(img_ori, item_index) 
            elif convert_type == 4: 
                self.flip_image(img_ori, item_index) 
            elif convert_type == 5: 
                self.blend_with_background_color(img_ori, item_index) 
            elif convert_type == 6: 
                self.flip_image_advanced(img_ori, item_index) 
            elif self.alternative_obj_index == self.MAX_REPLACEMENT: 
                pass
        cv2.imwrite(os.path.join("result_images/converted_image.jpg"), img_ori)
        pass
    
    def rotate_contour(self, contour, angle=180): 
        M = cv2.moments(contour)    
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00']) 
        rotation_matrix = cv2.getRotationMatrix2D((cx, cy), angle, 1) 
        rotated_contour = cv2.transform(contour.reshape(-1, 1, 2), rotation_matrix).reshape(-1, 2) 
        # print(rotated_contour) 
        return rotated_contour
    
    def get_color_contour(self, img_ori, item_index): 
        y = self.box[item_index][1] 
        x = self.box[item_index][0]
        M = cv2.moments(self.contours[item_index]) 
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00']) 
        color = (img_ori[y+cy, x+cx])
        b = int(color[0]) 
        g = int(color[1]) 
        r = int(color[2]) 
        return b, g, r

    def flip_image(self, img_ori, item_index): 
        x = self.box[item_index][0] 
        y = self.box[item_index][1] 
        w = self.box[item_index][2] 
        h = self.box[item_index][3] 
        roi = img_ori[y:y+h, x:x+w]
        flipped_roi = cv2.flip(roi, 0)
        img_ori[y:y+h, x:x+w] = flipped_roi
        
    def flip_image_advanced(self, img_ori, item_index=2): 
        b, g, r = self.get_color_contour(img_ori, item_index)
        self.blend_with_background_color(img_ori, item_index) 
        cont = self.contours[item_index]
        # print(cont)
        rotated_contour = self.rotate_contour(cont) 
        cv2.drawContours(img_ori, [rotated_contour], 0, (b, g, r), cv2.FILLED)
        pass
    
    def change_color_image(self, img_ori, item_index): 
        x = self.box[item_index][0] 
        y = self.box[item_index][1] 
        w = self.box[item_index][2] 
        h = self.box[item_index][3]  
        dst = cv2.bitwise_not(img_ori[y:y+h, x:x+w])  

        img_ori[y:y+h, x:x+w] = dst 
        

    def change_color_image_advanced(self, img_ori, item_index): 
        # print("contours:", self.contours[item_index])
        new_color = (np.random.uniform(0, 255), np.random.uniform(0, 255), np.random.uniform(0, 255))
        cv2.fillPoly(img_ori, [self.contours[item_index]], color=new_color)
        pass

    def replace_with_another_object(self, img_ori, item_index): 
        x = self.box[item_index][0] 
        y = self.box[item_index][1] 
        dir = 'alternative_objects/' 
        files = len(os.listdir(dir)) 
        print(files)
        random_object = random.randint(0, files - 1)
        prefix = 'alternative_objects/obj_' + str(random_object) + '.png'
        obj = cv2.imread(prefix, -1) 
        h, w, dst = self.insert_obj_to_img(obj, img_ori, y, x)
        img_ori[y:y+h, x:x+w] = dst 
        self.alternative_obj_index += 1
        pass

    def insert_obj_to_img(self, obj, img_ori, pos_y, pos_x): 
        # get the dimensions of the overlay image
        overlay_height, overlay_width, overlay_channels = obj.shape
        print("overlay", overlay_height, overlay_width)

        # create a copy of the overlay image with a 4th channel for alpha transparency
        overlay_image_with_alpha = np.zeros((overlay_height, overlay_width, 4), dtype=np.uint8)
        overlay_image_with_alpha[:, :, :3] = obj[:, :, :3]
        overlay_image_with_alpha[:, :, 3] = obj[:, :, 3] 

        # create a Region of Interest (ROI) for the overlay image
        roi = img_ori[pos_y:pos_y+overlay_height, pos_x:pos_x+overlay_width]

        # create a mask for the overlay image
        overlay_mask = overlay_image_with_alpha[:, :, 3]

        # invert the mask
        overlay_mask_inv = cv2.bitwise_not(overlay_mask)

        # apply the mask to the overlay image and the inverted mask to the ROI
        overlay_image_masked = cv2.bitwise_and(overlay_image_with_alpha, overlay_image_with_alpha, mask=overlay_mask)
        roi_masked = cv2.bitwise_and(roi, roi, mask=overlay_mask_inv)

        # combine the masked overlay image and the masked ROI using the add function
        output_roi = cv2.add(overlay_image_masked[:, :, :3], roi_masked) 
        return overlay_height, overlay_width, output_roi

        
    def blend_with_background_color(self, img_ori, item_index): 
        color = (img_ori[self.box[item_index][1], self.box[item_index][0]]) 
        b = int(color[0]) 
        g = int(color[1]) 
        r = int(color[2]) 
        print("b, g, r:", b, g, r)
        cv2.drawContours(img_ori, [self.contours[item_index]], 0,(b, g, r), cv2.FILLED)
        pass

    

