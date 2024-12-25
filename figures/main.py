import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


image = np.load("ps.npy.txt").astype("int")

top = np.array([[1, 1, 0, 0, 1, 1],
                [1, 1, 0, 0, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1]])

left = np.rot90(top)
bottom = np.rot90(left)
right = np.rot90(bottom)
filed = np.ones_like(top)

clone_image = label(image)
labels = np.unique(clone_image)

count = {"left": 0, "bottom": 0, "right": 0, "filed": 0}
print("Считаю")
for i in labels:
    extracted_shape = np.zeros_like(clone_image)
    extracted_shape[clone_image == i+12] = 1
    region = regionprops(extracted_shape)
    for i, prop in enumerate(region):
        mask = np.array(prop.image, dtype=int)
        if np.array_equal(mask, left):
            count["left"] += 1

        if np.array_equal(mask, bottom):
            count["bottom"] += 1

        if np.array_equal(mask, right):
            count["right"] += 1

        if np.array_equal(mask, filed):
            count["filed"] += 1
print("Готово")
print(f"Фигура: \n {left} \nвсего: {count['left']}")
print(f"Фигура: \n{bottom} \nвсего:{count['bottom']}")
print(f"Фигура: \n{right} \nвсего:{count['right']}")
print(f"Фигура: \n{filed} \nвсего:{count['filed']}")
print(f"Всего фигур: {labels.max()}")








