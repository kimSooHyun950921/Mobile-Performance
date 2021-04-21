import numpy as np
from scipy.signal.signaltools import correlate2d as c2d
import cv2 

def img_thresh(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_img, 215, 255, cv2.THRESH_BINARY)
    return (thresh-thresh.mean())/thresh.std()


def img_resize(scale_percent, img):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height),\
                     interpolation=cv2.INTER_AREA)
    return (img-img.mean())/img.std()


def sim(img1, img2, scale_percent=15, multichannel=True):
    '''sim: img1과 비교해서 img2와 얼마나 차이가 나는가'''
    img1 = img_thresh(img1)
    img2 = img_thresh(img2)

    re_im1 = img_resize(scale_percent, img1)
    re_im2 = img_resize(scale_percent, img2)

    c11 = c2d(re_im1, re_im1, mode='same').ravel().tolist()
    c12 = c2d(re_im1, re_im2, mode='same').ravel().tolist()
    print(np.nanmax(c12), np.nanmax(c11))
    if np.nanmax(c12) == np.nan:
        print(c11)
        print(c12)
    return np.nanmax(c12)/np.nanmax(c11)
        
