import autopy
import numpy as np
import cv2
import os
from matplotlib import pyplot as plt


def test():
    # captrue screen by specifing the position of game window
    os.system("screencapture -R110,400,300,300 screen.jpg")
    img = cv2.imread('screen.jpg')

    # find foregraound
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    sure_fg = cv2.bitwise_not(thresh)

    # erode to remove connection
    kernel = np.ones((13, 13), np.uint8)
    sure_fg = cv2.erode(sure_fg, kernel, iterations=1)

    # find center of each component
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        sure_fg)

    # remove head
    centroids = centroids[1:]
    centroids = centroids.astype(int)

    # get color from image
    centerColor = img[centroids[:, 1], centroids[:, 0]]
    colors = [0] * centroids.shape[0]

    # find the only different color by sorting
    for i, center in enumerate(centerColor):
        colors[i] = int(center[0]) - int(center[1]) - int(center[2])
    sortedColors = sorted(colors)

    # insure we have colors
    if len(sortedColors) > 3:
        diffColor = 0
        if sortedColors[0] != sortedColors[1]:
            diffColor = sortedColors[0]

        if sortedColors[len(sortedColors) - 1] != sortedColors[len(sortedColors) - 2]:
            diffColor = sortedColors[len(sortedColors) - 1]

        # if has diffcolor found
        if diffColor != 0:
            diffIndex = colors.index(diffColor)
            diffPoint = centroids[diffIndex]

            x = int(diffPoint[0]/2)
            y = int(diffPoint[1]/2)
            print(x, y)

            # move and click or use autopy.mouse.move(x, y)
            autopy.mouse.smooth_move(x + 110, y + 400)
            autopy.mouse.click()


while True:
    test()
