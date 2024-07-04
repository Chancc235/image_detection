import cv2
import numpy as np
from .seg import seg_img


def fix_image_size(image: np.array, expected_pixels: float = 2E6):
    ratio = expected_pixels / (image.shape[0] * image.shape[1])
    return cv2.resize(image, (0, 0), fx=ratio, fy=ratio)


def detect(image: np.array, threshold_blur=2, threshold_bright=1):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_map = cv2.Laplacian(image, cv2.CV_64F)
    imageVar = blur_map.var()

    img_shape = image.shape
    height, width = img_shape[0], img_shape[1]
    size = image.size
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    delta_sum = 0

    reduce_matrix = np.full((height, width), 128)
    shift_value = image - reduce_matrix
    shift_sum = np.sum(shift_value)
    da = shift_sum / size
    # 计算偏离128的平均偏差
    for i in range(256):
        delta_sum += (abs(i - 128 - da) * hist[i])
    ave = abs(delta_sum / size)
    # 亮度系数
    k = abs(da) / ave
    return blur_map, imageVar, k[0], bool(imageVar < threshold_blur), bool(k[0] < threshold_bright)


def detect_blurry(img, threshold_blur=2, threshold_bright=1):
    blur_map, score, brightness, blurry, bright = detect(img, threshold_blur=threshold_blur, threshold_bright=threshold_bright)
    if blurry:
        return blur_map, score, brightness, blurry, bright
    l = seg_img(img)
    blur_dic = {}
    for i in range(len(l)):
        _, _s, _, _b, _ = detect(l[i])
        if _b:
            blur_dic[i] = _s
    print(blur_dic)
    if len(blur_dic) >= 3 or (5 in blur_dic.keys() or 6 in blur_dic.keys()):
        blurry = True
    else:
        blurry = False
    return blur_map, score, brightness, blurry, bright


def pretty_blur_map(blur_map: np.array, sigma: int = 5, min_abs: float = 0.5):
    abs_image = np.abs(blur_map).astype(np.float32)
    abs_image[abs_image < min_abs] = min_abs

    abs_image = np.log(abs_image)
    cv2.blur(abs_image, (sigma, sigma))
    return cv2.medianBlur(abs_image, sigma)


if __name__ == '__main__':
    img = cv2.imread('D:/Blur/data/partial_blurry/285.png')
    img = fix_image_size(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(detect_blurry(gray))
