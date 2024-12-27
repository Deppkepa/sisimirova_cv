import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2hsv
from skimage.measure import label, regionprops

image = plt.imread('balls_and_rects.png')


binary = image.mean(axis=2) # Среднее по цветовым каналам
binary[binary > 0] = 1

labeled = label(binary)
regions = regionprops(labeled)

im_hsv = rgb2hsv(image)

color_counts = {}

for region in regions:
    minr, minc, maxr, maxc = region.bbox
    region_image = im_hsv[minr:maxr, minc:maxc]

    mean_hue = region_image[..., 0].mean()  # извлекает первый канал (оттенок - Hue)
    mean_saturation = region_image[..., 1].mean() # извлекает второй канал (насыщенность - Saturation)

    perimeter = region.perimeter
    area = region.area
    circularity = (4 * np.pi * area) / (perimeter ** 2) # вычисления степени округлости объекта
    if circularity > 0.8:
        shape = 'circles'
    else:
        shape = 'rectangles'
    hue_key = round(mean_hue, 2)
    if hue_key not in color_counts:
        color_counts[hue_key] = {'rectangles': 0, 'circles': 0}
    color_counts[hue_key][shape] += 1

for hue, counts in color_counts.items():
    print(f'Оттенок hsv: {hue:.2f} \n{counts} \n')

print(f"Общее количество фигур на изображении: {labeled.max()}")