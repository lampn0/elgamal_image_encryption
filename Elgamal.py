import array
import random
import cv2 as cv
import numpy
from matplotlib import pyplot as plt


# Read/Write image
# image_bin = open('txt_lena_image_bin.txt', 'w')
# image_int = open('txt_lena_image_int.txt', 'w')
# image_enc = open('txt_lena_image_enc.txt', 'w')
# image_dec = open('txt_lena_image_dec.txt', 'w')


# To find gcd of two numbers
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# For find primitive root i.e. random number
def find_primitive_root(q):
    l1: list[int] = []
    l2: list[int] = []
    for i in range(1, q):
        if gcd(q, i) == 1:
            l1.append(i)
    # print("Số n bất kỳ: ", q)
    # print("Các số nguyên tố với ", q, "là: ", l1)
    # print("Số các lớp đồng dư là: ", len(l1))

    i = 0
    j = 1
    while i < len(l1):
        while j <= len(l1):
            if ((l1[i] ** j) % q == 1) & (j < len(l1)):
                break
            elif ((l1[i] ** j) % q == 1) & (j == len(l1)):
                l2.append(l1[i])
            j = j + 1
        j = 1
        i = i + 1
    # print("Các phần tử nguyên thủy của ", q, "là: ", l2)
    return l2


# find prime
def check_prime_number(n):
    # flag = 0 => không phải số nguyên tố
    # flag = 1 => số nguyên tố
    flag = True
    if (n < 2):
        flag = False
        return flag

    for p in range(2, n):
        if n % p == 0:
            flag = False
            break
    return flag


# Load image
img = cv.imread('8-bit-256-x-256-Color-Lena-Image.png')

# p = input("Enter a large prime p = ")
# p = int(p)
flag = 0
while flag == 0:
    p = random.randint(1000, 2000)
    flag = check_prime_number(p)

print("p = ", p)

primitive_list = find_primitive_root(p)
print(primitive_list)
print("len = ", len(primitive_list))

i = random.randint(1, len(primitive_list) - 1)
e1 = primitive_list[i]
print("e1 = ", e1)

d = random.randint(1, p - 1)
print("d = ", d)
e2 = (e1 ** d) % p
print("e2 = ", e2)
# ==> Public key (e1, e2, p)
# ==> Private key d


# Alice send message M to Bob
encrypt = [[] for x in range(256)]
r = random.randint(1, p - 2)
C1 = (e1 ** r) % p
for i in range(256):
    for j in range(256):
        RGB = array.array('i', [0, 0, 0])
        P = img[i, j]
        C2 = ((e2 ** r) * P) % p
        img_bin0 = int(C2[0])
        img_bin1 = int(C2[1])
        img_bin2 = int(C2[2])
        RGB[0] = img_bin0
        RGB[1] = img_bin1
        RGB[2] = img_bin2
        encrypt[i].append(RGB)
encrypt = numpy.array(encrypt)
print(encrypt.shape)

# Decryption
decrypt = [[] for x in range(0, 256)]
C1 = int(C1)
d = int(p - 1 - d)
for i in range(0, 256):
    for j in range(0, 256):
        tmp = []
        C2 = encrypt[i, j]
        P = (C2 * (C1 ** d)) % p
        img_bin0 = int(P[2])
        img_bin1 = int(P[1])
        img_bin2 = int(P[0])
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
cv.imwrite("a.png", encrypt)
cv.imwrite("b.png", decrypt)
plt.show()

print('loading image successfully!')
