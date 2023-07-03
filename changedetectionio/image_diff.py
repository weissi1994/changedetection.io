# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2

# From https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
def render_diff(fpath_imageA, fpath_imageB):
    print(fpath_imageA)
    print(fpath_imageB)

    imageA = cv2.imread(fpath_imageA, cv2.IMREAD_COLOR)
    imageB = cv2.imread(fpath_imageB, cv2.IMREAD_COLOR)

    heightA = imageA.shape[0]
    heightB = imageB.shape[0]

    if heightA > heightB:
        imageA = imageA[-heightB:, :]
    if heightB > heightA:
        imageB = imageB[-heightA:, :]
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
           cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # loop over the contours
    for c in cnts:
           # compute the bounding box of the contour and then draw the
           # bounding box on both input images to represent where the two
           # images differ
           (x, y, w, h) = cv2.boundingRect(c)
           cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
           cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # return cv2.imencode('.jpg', imageB)[1].tobytes()
    return cv2.imencode('.jpg', imageA)[1].tobytes()
