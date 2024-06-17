from dct import DCT
import cv2
import os

def encode(imagepath, secret):
    """
    Encodes a secret message into an image using the DCT (Discrete Cosine Transform) algorithm.

    Args:
        imagepath (str): The path to the original image file.
        secret (str): The secret message to be encoded.

    Returns:
        str: The path to the encoded image file.

    Raises:
        None

    This function reads the original image file using OpenCV's `imread` function and converts it to an unchanged format. 
    It then creates an instance of the `DCT` class and calls its `encode_image` method to encode the secret message into the image. 
    The encoded image is saved with a prefix of "dct_" followed by the original image file name. 
    The function returns the path to the encoded image file.
    """
    dct = DCT()
    original_image_file = imagepath
    dct_img = cv2.imread(original_image_file, cv2.IMREAD_UNCHANGED)
    secret_msg = secret
    print("The message length is: ", len(secret_msg))
    dct_img_encoded = dct.encode_image(dct_img, secret_msg)
    dct_encoded_image_file = "dct_" + os.path.basename(original_image_file)
    encoded_image_path = os.path.join('Encoded_image', dct_encoded_image_file)
    cv2.imwrite(encoded_image_path, dct_img_encoded)
    print("Encoded images were saved!")
    return encoded_image_path
