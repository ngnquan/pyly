import cv2
import numpy as np

from PIL import Image

# read image
def imread(impath):
    stream = open(impath, "rb")
    bytes = bytearray(stream.read())
    numpyarray = np.asarray(bytes, dtype=np.uint8)
    img = cv2.imdecode(numpyarray, cv2.IMREAD_COLOR)
    return img

# write image
def imwrite(path, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    out = Image.fromarray(image)
    out.save(path)
