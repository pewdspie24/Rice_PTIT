import cv2
from cv2 import imshow
from cv2 import ROTATE_90_CLOCKWISE
import numpy as np
import glob
import os
import tqdm

def crop_minAreaRect(img, rect):
    """
    Summary: this function return a cropped portion of an image based on cv2.minAreaRect().
    Output: cropped rice leaf image.
    """
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img, M, (width, height))
    if warped.shape[0] > warped.shape[1]:
        warped = cv2.rotate(warped, ROTATE_90_CLOCKWISE)

    return warped

def cut_img(mask_path):
    """
    Summary: this function find contour on a processed image(background removed) then cut the original image accordingly.
    Output: cropped rice leaf image.
    """
    img_path = mask_path.replace("rice_mask", "rice")
    
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # find contour
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # filter small contour
    all_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 7000:
            all_contours.append(contour)

    img = cv2.imread(img_path)
    # apply image cropping
    for cnt in all_contours:
        rect = cv2.minAreaRect(cnt)
        cropped = crop_minAreaRect(img, rect)
    
        cv2.imwrite(mask_path.replace("rice_mask", "cropped"), cropped)
if __name__ == "__main__":
    DIR = r"Data\rice_mask\**\*"
    # process all image in rice dataset
    for path in tqdm.tqdm(glob.glob(DIR, recursive=True)):
        if not os.path.isdir(path):
            cut_img(os.path.normpath(path))
