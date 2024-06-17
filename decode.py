from dct import DCT
import cv2
import os

def decode(imagepath):
    dct = DCT()
    dct_img = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)
    dct_hidden_text = dct.decode_image(dct_img)
    print(dct_hidden_text)
    return dct_hidden_text
