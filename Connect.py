import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import array
import random
import cv2 as cv
import numpy


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
    # l2: list[int] = []
    for i in range(1, q):
        if gcd(q, i) == 1:
            l1.append(i)

    i = 3000
    j = 1
    while i < len(l1):
        while j <= len(l1):
            if ((l1[i] ** j) % q == 1) & (j < len(l1)):
                break
            elif ((l1[i] ** j) % q == 1) & (j == len(l1)):
                # l2.append(l1[i])
                return l1[i]
            j = j + 1
        j = 1
        i = i + 1
    # print("Các phần tử nguyên thủy của ", q, "là: ", l2)
    # return l2


# find prime
def check_prime_number(n):
    # flag = 0 => không phải số nguyên tố
    # flag = 1 => số nguyên tố
    flag = True
    if n < 2:
        flag = False
        return flag

    for i in range(2, n):
        if n % i == 0:
            flag = False
            break
    return flag


def load_image(link):
    # Load image
    # img = cv.imread('8-bit-256-x-256-Color-Lena-Image.png')
    img = cv.imread(link)
    return img


def random_key():
    flag = 0
    while flag == 0:
        p = random.randint(6000, 8000)
        flag = check_prime_number(p)
    return p


def key_gen(p):
    e1 = find_primitive_root(p)
    d = random.randint(1, p - 1)
    e2 = (e1 ** d) % p
    return e1, e2, d
    # ==> Public key (e1, e2, p)
    # ==> Private key d


# Alice send message M to Bob
def encryption(img, p, e1, e2):
    global encrypt
    encrypt = [[] for x in range(256)]
    r = random.randint(1, p - 2)
    c1 = (e1 ** r) % p
    for i in range(256):
        for j in range(256):
            rgb = array.array('i', [0, 0, 0])
            u = img[i, j]
            c2 = ((e2 ** r) * u) % p
            img_bin0 = int(c2[0])
            img_bin1 = int(c2[1])
            img_bin2 = int(c2[2])
            rgb[0] = img_bin0
            rgb[1] = img_bin1
            rgb[2] = img_bin2
            encrypt[i].append(rgb)
    encrypt = numpy.array(encrypt)
    cv.imwrite("encrypt.png", encrypt)
    return c1, r, encrypt


# Decryption
def decryption(c1, p, d):
    decrypt = [[] for x in range(0, 256)]
    c1 = int(c1)
    d = int(p - 1 - d)
    for i in range(0, 256):
        for j in range(0, 256):
            tmp = []
            c2 = encrypt[i, j]
            u = (c2 * (c1 ** d)) % p
            img_bin0 = int(u[2])
            img_bin1 = int(u[1])
            img_bin2 = int(u[0])
            tmp.append(img_bin2)
            tmp.append(img_bin1)
            tmp.append(img_bin0)
            decrypt[i].append(tmp)
    decrypt = numpy.array(decrypt)
    cv.imwrite("decrypt.png", decrypt)


# from giaodienmahoa import Ui_Dialog
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("giaodienmahoa.ui", self)
        self.browser.clicked.connect(self.browserfiles)
        self.khoangaunhien.clicked.connect(self.khoaNgauNhien)
        self.tuychinhkhoa.clicked.connect(self.tuyChinhKhoa)
        self.lammoikhoa.clicked.connect(self.lamMoiKhoa)
        self.mahoa.clicked.connect(self.encrypt_img)
        self.giaima.clicked.connect(self.decrypt_img)
        self.refresh.clicked.connect(self.refresh_bt)

    def browserfiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'Images (*.png)')
        self.anhgoc.setPixmap(QPixmap(fname[0]))
        self.txtLink.setText(fname[0])

    def khoaNgauNhien(self):
        p = random_key()
        self.p.setText(str(p))
        e1, e2, d = key_gen(p)
        self.e1.setText(str(e1))
        self.e2.setText(str(e2))
        self.d.setText(str(d))

    def tuyChinhKhoa(self):
        p = self.p.toPlainText()
        p = int(p)
        check = check_prime_number(p)
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Kiểm tra số nguyên tố")
        if check:
            e1, e2, d = key_gen(p)
            self.e1.setText(str(e1))
            self.e2.setText(str(e2))
            self.d.setText(str(d))
            msg.setText("Bạn đã chọn p đúng ^-^")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()
        else:
            msg.setText("p không phải là số nguyên tố. Bạn hãy nhập lại !!!")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            self.lamMoiKhoa()
            msg.exec_()

    def lamMoiKhoa(self):
        self.p.clear()
        self.e1.clear()
        self.e2.clear()
        self.d.clear()
        self.r.clear()
        self.c1.clear()

    def encrypt_img(self):
        p = int(self.p.toPlainText())
        e1 = int(self.e1.toPlainText())
        e2 = int(self.e2.toPlainText())
        link = self.txtLink.text()
        img = load_image(str(link))
        print("Load ảnh thành công")
        c1, r, encrypt = encryption(img, p, e1, e2)
        self.r.setText(str(r))
        self.c1.setText(str(c1))
        self.anhmahoa.setPixmap(
            QPixmap('D:/workspace/lampn182628/ly_thuyet_mat_ma/project/elgamal_image_encryption/encrypt.png'))
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Mã hóa")
        msg.setText("Mã hóa thành công")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()

    def decrypt_img(self):
        p = int(self.p.toPlainText())
        d = int(self.d.toPlainText())
        c1 = int(self.c1.toPlainText())
        decryption(c1, p, d)
        self.anhgiaima.setPixmap(
            QPixmap('D:/workspace/lampn182628/ly_thuyet_mat_ma/project/elgamal_image_encryption/decrypt.png'))
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Giải mã")
        msg.setText("Giải mã thành công")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()

    def refresh_bt(self):
        self.lamMoiKhoa()
        self.anhgoc.clear()
        self.anhmahoa.clear()
        self.anhgiaima.clear()


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1100)
widget.setFixedHeight(860)
widget.show()
sys.exit(app.exec_())
