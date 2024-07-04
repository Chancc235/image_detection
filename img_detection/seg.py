import cv2


def seg_img(img):
    h = img.shape[0]
    w = img.shape[1]
    ww = int(w / 4)
    hh = int(h / 3)

    point = [(0, 0), (0, ww), (0, 2 * ww), (0, 3 * ww),
             (hh, 0), (hh, ww), (hh, 2 * ww), (hh, 3 * ww),
             (2 * hh, ww), (2 * hh, 2 * ww), (2 * hh, 3 * ww)]

    l = []

    for i in range(len(point)):
        l.append(img[point[i][0]:point[i][0] + hh, point[i][1]:point[i][1] + ww])

    return l

