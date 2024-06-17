from dct import DCT
import cv2
import os

def decode(imagepath):
    dct = DCT()
    dct_img = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)
    encrypted_secret = dct.decode_image(dct_img)
    return encrypted_secret