import os
import pandas as pd
from pathlib import Path
import cv2
import numpy as np
ROOT_DIR = "root"

def process(mode="train"):
    # filenames = []
    if mode == "train":
        root_dir = os.path.join(ROOT_DIR, "train")
    else:
        root_dir = os.path.join(ROOT_DIR, "validation")
    filepaths = []
    categories = []
    for subdirs, dirs, files in os.walk(root_dir):
        images = Path(subdirs).glob('*.jpg')
        for image in images:
            if subdirs.endswith("BrownSpot"):
                categories.append(0.)
            elif subdirs.endswith("Healthy"):
                categories.append(3.)
            elif subdirs.endswith("Hispa"):
                categories.append(1.)
            elif subdirs.endswith("LeafBlast"):
                categories.append(2.)
            filename = str(image)
            filepaths.append(filename)
            # filenames.append(filename.split("\\")[-1])

    df = pd.DataFrame({
        'filepath': filepaths,
        'category': categories
    })
    # df['category'] = df['category'].replace({0:"brownspot", 1:"hispa", 2:"leafblast", 3:"healthy"})
    return df


test_path = r""

"""
NOTE: main func == color_masking

TODO:
    - tối ưu lại remove_shades: có thể k khả thi lắm do data
    - tối ưu findContours trong color_masking():
        + nếu contourArea > threshold nhất định mới lưu
        + vẫn còn các trường hợp bắt nhỏ lẻ (lỗi ở bóng)
        + (idea) có thể kết hợp inRange + contourArea: chỉ lấy nx phần có màu != xám
    - xắp xếp lại code
"""


class ImagePreprocessing:
    def __init__(self) -> None:
        pass

    def fix_resolution(self, img=None, size=(1280, 720)):
        cv2.namedWindow("test", cv2.WINDOW_NORMAL)
        imS = cv2.resize(img, size)
        return imS

    def remove_shades(self, path=test_path):
        img = cv2.imread(path)
        hsv = img.copy()
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV_FULL)

        # absDiff method
        rgb_planes = cv2.split(img)
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 11)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(
                diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_norm_planes.append(norm_img)
        shadowRemoved = cv2.merge(result_norm_planes)
        # shadeHsv = cv2.cvtColor(shadowRemoved, cv2.COLOR_BGR2HSV_FULL)

        # bg Subtractor
        # NOTE: k bắt được lúa
        # fgbg = cv2.createBackgroundSubtractorMOG2(256, cv2.THRESH_BINARY_INV, 1)
        # masked_image = fgbg.apply(img)
        # masked_image[masked_image==127] = 0

        # show results
        cv2.imshow("origin", cv2.resize(img, None, fx=.5, fy=.5))
        cv2.imshow("no shadow", cv2.resize(shadowRemoved, None, fx=.5, fy=.5))
        if cv2.waitKey(0) and 0xFF == ord("q"):
            cv2.destroyAllWindows()

        """
        NOTE: k tốt lắm, xóa cả viền của lá dẫn tới việc k khoanh đc contour
        """
        # return shadeHsv

    def color_masking(self, path=test_path):
        img = cv2.imread(path)
        img1 = img.copy()

        # img1 = cv2.GaussianBlur(img1, (9, 9), 3)
        hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV_FULL)

        # get shade-removed img
        noShade = self.remove_shades()

        # Filter out low saturation values, which means gray-scale pixels(majorly in background)
        bgd_mask = cv2.inRange(hsv, np.array(
            [0, 0, 0]), np.array([255, 30, 255]))
        white_bg = cv2.inRange(hsv, np.array(
            [0, 0, 0]), np.array([255, 255, 255]))
        mask = cv2.bitwise_xor(white_bg, bgd_mask)

        # cv2.imshow("bgd masked", cv2.resize(bgd_mask, None, fx=.4, fy=.4))
        # cv2.imshow("white", cv2.resize(white_bg, None, fx=.4, fy=.4))
        # cv2.imshow("mask", cv2.resize(mask, None, fx=.4, fy=.4))

        # testing filtering fray
        grey_upr = np.array([0, 0, 100])
        grey_lwr = np.array([0, 0, 0])

        # testing
        shade_mask = cv2.inRange(hsv, grey_lwr, grey_upr)
        # all_shade_mask = cv2.inRange(noShade, np.array([0, 0, 0]), np.array([255, 255, 255]))
        # m_mask = cv2.bitwise_xor(shade_mask, all_shade_mask)

        # find contours on mask
        contours, _ = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # append all contours if contour area is large enough
        all_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1500:
                all_contours.append(contour)

        # draw contours
        img1 = img.copy()
        for i in range(len(all_contours)):
            img1 = cv2.drawContours(img1, all_contours, i, [0, 255, 0], 2)
        print(len(all_contours))

        # check contours
        # f = open("log.txt", 'w')
        # for row in all_contours[0]:
        #     print(row, file=f)
        # img1 = cv2.drawContours(img1, all_contours, 0, [0, 255, 0], 2)

        # show results
        # cv2.imshow("bgd masked", cv2.resize(bgd_mask, None, fx=.4, fy=.4))
        cv2.imshow("origin", cv2.resize(img, None, fx=.4, fy=.4))
        # cv2.imshow("mask", cv2.resize(mask, None, fx=.4, fy=.4))
        cv2.imshow("hsv", cv2.resize(hsv, None, fx=.4, fy=.4))
        cv2.imshow("contours", cv2.resize(img1, None, fx=.5, fy=.5))

        # # testing
        # cv2.imshow("all mask", cv2.resize(white_bg, None, fx=.4, fy=.4))
        # cv2.imshow("bgd", cv2.resize(bgd_mask, None, fx=.4, fy=.4))

        if cv2.waitKey(0) and 0xFF == ord("q"):
            cv2.destroyAllWindows()

        """
        TODO:
            - Contour sẽ bao viền ngoài của object nếu object ngoài frame (bị thiếu)
            - Dính bóng nặng (blur với format màu thường có thể fix đc nhưng hsv thì chưa)

        IDEAS: ?
            - Có thể tweak bgd_mask, bắt đc thêm gray (bóng)
        """

    def thresholding(self, path=test_path):
        img = cv2.imread(path)
        img1 = cv2.medianBlur(img.copy(), 7)

        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 17, 10)
        # ret, thresh = cv2.threshold(self.img1, 110, 255, 0)
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # draw contours
        img1 = cv2.drawContours(img.copy(), contours, -1, [0, 255, 0], 2)

        # bb
        # rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # cv2.drawContours(self.img, [box], -1, (255, 0, 0), 2)

        # centered line
        # rows,cols = self.img.shape[:2]
        # [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
        # lefty = int((-x*vy/vx) + y)
        # righty = int(((cols-x)*vy/vx)+y)
        # cv2.line(self.img,(cols-1,righty),(0,lefty),(0,255,0),2)

        cv2.imshow("frame", cv2.resize(img1, None, fx=.4, fy=.4))
        cv2.imshow("origin", cv2.resize(img, None, fx=.4, fy=.4))
        if cv2.waitKey(0) and 0xFF == ord("q"):
            cv2.destroyAllWindows()

    def otsu_thresholding(self, path=test_path):

        img = cv2.imread(path, 0)
        img1 = img.copy()
        # self.img1 = cv2.GaussianBlur(self.img1, (5, 5), 0)
        img1 = cv2.medianBlur(img1, 13)

        # calculate otsu thresholding
        threshold, ret = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        img = cv2.imread(path)
        hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        # find contours
        contours, _ = cv2.findContours(
            ret, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        print(len(contours))

        # draw contours
        img1 = img.copy()
        for i in range(len(contours)):
            img1 = cv2.drawContours(img1, contours, i, [0, 255, 0], 2)

        # draw centered line
        # rows,cols = self.img.shape[:2]
        # [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
        # lefty = int((-x*vy/vx) + y)
        # righty = int(((cols-x)*vy/vx)+y)
        # cv2.line(self.img,(cols-1,righty),(0,lefty),(0,255,0),2)

        # bb
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img1, [box], -1, (255, 0, 0), 4)

        # show image
        cv2.imshow("origin", cv2.resize(img, None, fx=.4, fy=.4))
        cv2.imshow("hsv", cv2.resize(hsvimg, None, fx=.3, fy=.3))
        cv2.imshow("frame", cv2.resize(img1, None, fx=.4, fy=.4))
        if cv2.waitKey(0) and 0xFF == ord("q"):
            cv2.destroyAllWindows()


if __name__ == "__main__":

    processer = ImagePreprocessing()
    # processer.thresholding()
    # processer.otsu_thresholding()
    # processer.color_masking()
    processer.remove_shades()
