import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def process_image(file_path):
    image = plt.imread(file_path)
    binary = np.float64(image.mean(axis=2))
    binary[binary <= 150] = 1
    binary[binary > 150] = 0
    labels = label(binary)
    return regionprops(labels)

def count_pencils(directory):
    files = os.listdir(directory)
    count_all = 0
    for file in files:
        file_path = os.path.join(directory, file)
        if not file.lower().endswith(('.jpg')):
            continue
        regions = process_image(file_path)
        pencils = sum(1 for value in regions if value.area > 150000 and value.eccentricity > 0.95)
        count_all += pencils
        print(f"Итого карандашей: {file}: {pencils}")
    print("Всего:", count_all)

directory = "output_images/"
count_pencils(directory)
