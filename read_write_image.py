import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

image_bin = open('txt_test_image_bin2.txt', 'w+')
image_int = open('txt_test_image_int2.txt', 'w+')

# Load and blur image
img = cv.imread('anh_test_RGB2.jpg')
for i in range(0, 300):
    for j in range(0, 300):
        pixel = img[i, j]
        print("pixel: ", pixel)
        pixel_bin0 = bin(pixel[0])
        pixel_bin1 = bin(pixel[1])
        pixel_bin2 = bin(pixel[2])
        pixel_bin0 = pixel_bin0[2:]
        pixel_bin1 = pixel_bin1[2:]
        pixel_bin2 = pixel_bin2[2:]
        if len(pixel_bin0) == 7:
            pixel_bin0 = '0' + pixel_bin0
        if len(pixel_bin1) == 7:
            pixel_bin1 = '0' + pixel_bin1
        if len(pixel_bin2) == 7:
            pixel_bin2 = '0' + pixel_bin2
        image_bin.write(pixel_bin0+' '+pixel_bin1+' '+pixel_bin2+'\n')
        image_int.write(str(pixel[0])+' '+str(pixel[1])+' '+str(pixel[2])+'\n')
blur = cv.GaussianBlur(img, (5, 5), 0)

# Convert color from bgr (OpenCV default) to rgb
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
blur_rgb = cv.cvtColor(blur, cv.COLOR_BGR2RGB)

# Display
plt.subplot(121), plt.imshow(img_rgb), plt.title('Gauss Noise 2')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur_rgb), plt.title('Gauss Noise - Blurred 2')
plt.xticks([]), plt.yticks([])
plt.show()