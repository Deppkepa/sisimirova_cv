import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1
def t(x,y,size):
    return (x + y) / (2 * size)
def gradient_line(image):
    for i, v in enumerate(np.linspace(0, 1, image.shape[0])):
        r = lerp(color1[0], color2[0], v)
        g = lerp(color1[1], color2[1], v)
        b = lerp(color1[2], color2[2], v)
        image[i, :, :] = [r, g, b]
def gradient_45(image):
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            r = lerp(color1[0], color2[0], t(x, y, image.shape[0]))
            g = lerp(color1[1], color2[1], t(x, y, image.shape[0]))
            b = lerp(color1[2], color2[2], t(x, y, image.shape[0]))
            image[x, y] = [b, g, r]

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]
image_copy = image
color1 = [255, 128, 0]
color2 = [0, 128, 255]

plt.figure(1)
plt.subplot(121)
gradient_line(image)
plt.imshow(image, vmin=50, vmax=100)
plt.title("Прямой градиент")

plt.subplot(122)
gradient_45(image_copy)
plt.imshow(image_copy, vmin=50, vmax=100)
plt.title("Косой градиент")
plt.show()
