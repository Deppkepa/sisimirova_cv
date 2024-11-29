import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion


def neighbours2(y, x):
    return (y, x - 1), (y - 1, x)


def exist(B, nbs):
    left, top = nbs
    if (left[0] >= 0 and left[0] < B.shape[1] and
            left[1] >= 0 and left[1] < B.shape[0]):
        if B[left] == 0:
            left = None
    else:
        left = None
    if (top[0] >= 0 and top[0] < B.shape[1] and
            top[1] >= 0 and top[1] < B.shape[0]):
        if B[top] == 0:
            top = None
    else:
        top = None

    return left, top


def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j


def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)

    if j != k:
        linked[k] = j


def two_pass(B):  # маркировка связных компонент
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype='uint')
    label = 1
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                nbs = neighbours2(y, x)
                existed = exist(B, nbs)

                if existed[0] is None and existed[1] is None:
                    m = label
                    label += 1
                else:

                    lbs = [LB[n] for n in existed if n is not None]

                    m = min(lbs)

                LB[y, x] = m
                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:

                new_label = find(LB[y, x], linked)
                if new_label != LB[y, x]:
                    LB[y, x] = new_label
    LB_copy = LB
    for n, y in enumerate(np.unique(LB)):
        LB_copy[LB == y] = n
    return LB


def split_wires(B):
    num_wires = np.unique(B)
    struct = np.ones((3, 1))
    result = []
    for i in num_wires:
        if i == 0:
            continue
        else:
            wire = B == i
            eroded_wire = binary_erosion(wire, struct)
            result.append(eroded_wire)
    return result


def count_torn(wire):
    wire = np.array(wire, dtype="uint8")
    count = wire.shape[1] - len(wire[wire == 1])
    return count


for n in range (1, 6):
    print(f"wires{n}npy.txt")
    image = two_pass(np.load(f"wires{n}npy.txt").astype("uint8"))
    splitted_wire = split_wires(image)
    for i in range(len(splitted_wire)):
        parts = count_torn(splitted_wire[i])
        if (parts == 0):
            print("Провод целый")
        elif (parts >= splitted_wire[i].shape[1]):
            print("Провод дефектный")
        else:
            print(f"Провод {i + 1} на изображении разделен на {parts} частей")

    plt.imshow(image)
    plt.show()
