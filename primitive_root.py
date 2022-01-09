import random
from math import pow
from typing import List


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
    print("Số n bất kỳ: ", q)
    print("Các số nguyên tố với ", q, "là: ", l1)
    print("Số các lớp đồng dư là: ", len(l1))

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

    print("Các phần tử nguyên thủy của ", q, "là: ", l2)


find_primitive_root(14)
