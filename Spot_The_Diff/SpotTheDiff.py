import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog
from skimage.measure import compare_ssim

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15
differences = 0


def alignImages(im1, im2):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h


def readpic1(self):
    filename = QFileDialog.getOpenFileName()
    path = filename[0]
    self.picture1.setPixmap(QtGui.QPixmap(path))
    self.im1 = cv2.imread(path)


def readpic2(self):
    filename = QFileDialog.getOpenFileName()
    path = filename[0]
    self.picture2.setPixmap(QtGui.QPixmap(path))
    self.im2 = cv2.imread(path)


def spot_diff(self):
    global differences
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    im1, _ = self.alignImages(self.im1, self.im2)
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    ksize = (3, 3)

    img1 = cv2.blur(im1, ksize)
    img1 = cv2.GaussianBlur(img1, (5, 5), 250)

    img1 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    im2 = cv2.cvtColor(self.im2, cv2.COLOR_BGR2GRAY)
    ksize = (3, 3)

    img2 = cv2.blur(im2, ksize)
    img2 = cv2.GaussianBlur(img2, (5, 5), 250)

    img2 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    (score, diff) = compare_ssim(img1, img2, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    _, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        if 500 < cv2.contourArea(c) < 1000:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(self.im1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.rectangle(self.im2, (x, y), (x + w, y + h), (255, 0, 0), 2)
            differences += 1

    # show the output images

    self.numbervalue.setText(str(self.differences))
    cv2.imshow("im1", self.im1)
    cv2.imshow("im2", self.im2)
    cv2.waitKey(0)
