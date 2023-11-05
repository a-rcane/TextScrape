import time

import keras_ocr
import cv2


def img_to_txt():
    pipeline = keras_ocr.pipeline.Pipeline()

    image = cv2.imread('Temp/25-homepage-logos.png')

    images = [image]
    prediction_groups = pipeline.recognize(images)

    print(f"{prediction_groups}")

    return prediction_groups


start = time.time()
img_to_txt()
end = time.time()
total = end - start

print(f"{total} seconds")
