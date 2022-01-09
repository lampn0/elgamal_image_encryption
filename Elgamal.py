import array
import random
import itertools
import cv2 as cv
import numpy
from matplotlib import pyplot as plt
from matplotlib import image as im

# Read/Write image
# image_bin = open('txt_lena_image_bin.txt', 'w')
# image_int = open('txt_lena_image_int.txt', 'w')
# image_enc = open('txt_lena_image_enc.txt', 'w')
# image_dec = open('txt_lena_image_dec.txt', 'w')


# Load image
img = cv.imread('8-bit-256-x-256-Color-Lena-Image.png')


# p = input("Enter a large prime p = ")
# p = int(p)
check = 1
while check:
    p = random.randint(10**3, 10**5)
    for i in range(1, p-1):
        if p % i == 0:
            check == 1
            print("Not prime number !!!")
            continue
        else:
            check = 0
    print("OK. This is prime number !!!")

d = random.randint(1, p-1)
e1 = random.randint(1, p-2)
e2 = (e1**d) % p
# ==> Public key (e1, e2, p)
# ==> Private key d

# Alice send message M to Bob
encrypt = [[] for x in range(256)]
r = random.randint(1, p-2)
C1 = (e1**r) % p
for i in range(256):
    for j in range(256):
        RGB = array.array('i', [0,0,0])
        P = img[i, j]
        C2 = ((e2**r) * P) % p
        img_bin0 = int(C2[0])
        img_bin1 = int(C2[1])
        img_bin2 = int(C2[2])
        RGB[2] = img_bin0
        RGB[1] = img_bin1
        RGB[0] = img_bin2
        encrypt[i].append(RGB)
encrypt = numpy.array(encrypt)
print(encrypt.shape)

# im.imsave('a.png', encrypt[::1])
# print(encrypt[::1])


# Decryption
decrypt = [[] for x in range(0, 256)]
C1 = int(C1)
d = int(p-1-d)
for i in range(0, 256):
    for j in range(0, 256):
        tmp = []
        C2 = encrypt[i, j]
        P = (C2*(C1**d)) % p
        img_bin0 = int(P[0])
        img_bin1 = int(P[1])
        img_bin2 = int(P[2])
        tmp.append(img_bin2)
        tmp.append(img_bin1)
        tmp.append(img_bin0)
        decrypt[i].append(tmp)
decrypt = numpy.array(decrypt)
print(decrypt)

# plt.savefig("a.png",encrypt ,dpi='figure')
# plt.subplot(121), plt.imshow(encrypt), plt.title('Encryption')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(decrypt), plt.title('Decryption')
# plt.xticks([]), plt.yticks([])
cv.imwrite("b.png", encrypt)
cv.imwrite("a.png", decrypt)
plt.show()

print('loading image successfully!')