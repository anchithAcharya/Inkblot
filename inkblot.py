import numpy as np
from opensimplex import noise3array, random_seed, seed as os_seed
from PIL import Image


IMG_DIM_X = 1000
IMG_DIM_Y = 500


def gen_noise(seed = None):
    x_y_axis = np.arange(0,IMG_DIM_X/2)/100
    if seed: os_seed(seed)
    else: random_seed()

    return noise3array(x_y_axis, x_y_axis, x_y_axis*10)


def depth(x,y):
    nx = (2*x/IMG_DIM_X - 1 )
    ny = 2*y/IMG_DIM_Y - 1

    d = (1-nx**2) * (1-ny**2)
    return d

def gen_img(noise):
    img = Image.new('RGB', (IMG_DIM_X, IMG_DIM_Y), 'white')

    for i, row in enumerate(noise):
        for j, value in enumerate(row):
            d = depth(i,j)
            value = (value+1)/2
            value = int(value * 256 * d)
            if value > 128:
                value = 0
                img.putpixel((i,j), (value, value, value))
                img.putpixel((-i-1,j), (value, value, value))

    return img


noise = gen_noise()
imgs = []

for frame in range(10):
  img = gen_img(noise[frame])
  imgs.append(img)

imgs[0].save('rorschach.webp', save_all=True, append_images=imgs[1:], )