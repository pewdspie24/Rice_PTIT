import os
import cv2
import matplotlib.pyplot as plt
import skimage.io as io
import numpy as np

class ImagePreprocessing:
    def __init__(self) -> None:
        pass

    def color_masking(self, path, des_path, mode = "colab"):
        if mode == "colab":
            img = cv2.imread(path) # for processing
        else:
            img = io.imread(path) # for display
        img_tmp_1 = img.copy()

        #* Convert image. RGB -> HSV (Hue, Saturation, Value)
        hsv = cv2.cvtColor(img_tmp_1, cv2.COLOR_BGR2HSV_FULL)

        #* Filter out low saturation values, which means gray-scale pixels(majorly in background)
        bgd_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([255, 80, 255]))
        white_bg = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([255, 255, 255]))
        mask = cv2.bitwise_xor(white_bg, bgd_mask)

        #* Find contours on mask
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #* Append all contours if contour area is large enough
        #? There is another way to approach: Sort contours then choose the largest one.
        all_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
        if area > 7000:
            all_contours.append(contour)

        #* Draw contours
        img_fully_filled = img.copy()
        img_outlines_filled = img.copy()
        img_tmp_2 = img.copy()
        img_fully_filled = cv2.drawContours(img_fully_filled, all_contours, -1, [0, 255, 0], -1)
        img_outlines_filled = cv2.drawContours(img_outlines_filled, contours, -1, [255, 0, 0], 2)
        
        #* Filter leaf's portion
        mask_black = np.zeros_like(mask)
        mask_black = cv2.drawContours(mask_black, all_contours, -1, 255, -1)
        out_black = np.zeros_like(img_tmp_2)
        out_black[mask_black == 255] = img_tmp_2[mask_black == 255]
        
        #* Save filtered image
        if mode == "colab":
            cv2.imwrite(des_path ,out_black)

        else:
            #* Show image
            rows, columns = 2, 4
            fig = plt.figure(figsize=(10, 7))

            #* Adds a subplot at the 2nd position
            fig.add_subplot(rows, columns, 1)
            plt.imshow(img)
            plt.axis('off')
            plt.title("origin")
            
            #* Adds a subplot at the 2nd position
            fig.add_subplot(rows, columns, 2)
            plt.imshow(hsv)
            plt.axis('off')
            plt.title("hsv")
            
            #* Adds a subplot at the 3rd position
            fig.add_subplot(rows, columns, 3)
            plt.imshow(bgd_mask)
            plt.axis('off')
            plt.title("bgd_mask")
            
            #* Adds a subplot at the 4th position
            fig.add_subplot(rows, columns, 4)
            plt.imshow(mask)
            plt.axis('off')
            plt.title("mask")

            #* Adds a subplot at the 4th position
            fig.add_subplot(rows, columns, 5)
            plt.imshow(img_outlines_filled)
            plt.axis('off')
            plt.title("All contours")

            #* Adds a subplot at the 4th position
            fig.add_subplot(rows, columns, 6)
            plt.imshow(img_fully_filled)
            plt.axis('off')
            plt.title("Fully filled contour")

            #* Adds a subplot at the 4th position
            fig.add_subplot(rows, columns, 7)
            plt.imshow(out_black)
            plt.axis('off')
            plt.title("Final result")
        
        # cv2.imshow("bgd_masked", cv2.resize(bgd_mask, None, fx=.4, fy=.4))
        # cv2.imshow("origin", cv2.resize(img, None, fx=.4, fy=.4))
        # cv2.imshow("mask", cv2.resize(mask, None, fx=.4, fy=.4))
        # cv2.imshow("hsv", cv2.resize(hsv, None, fx=.4, fy=.4))
        # cv2.imshow("contours", cv2.resize(img1, None, fx=.4, fy=.4))
        # cv2.imshow("all mask", cv2.resize(white_bg, None, fx=.4, fy=.4))
    # if cv2.waitKey(0) and 0xFF == ord("q"):
        #   cv2.destroyAllWindows()

dir_train = "C:/Users/Admin/Downloads/IMG_2992.jpg"
dir_des = "C:/Users/Admin/Downloads/IMG_2992_masked.jpg"
mode = "test"

if __name__ == "__main__":
    processer = ImagePreprocessing()
    processer.color_masking(dir_train, dir_des, mode)