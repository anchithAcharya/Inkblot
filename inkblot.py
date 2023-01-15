import tkinter as tk
import numpy as np
from opensimplex import noise3array, random_seed
from PIL import Image, ImageTk


IMG_DIM_X = 1000
IMG_DIM_Y = 500
SHIFT_SPEED = 0.05


random_seed()
x_y_axis = np.arange(0,IMG_DIM_X/2)/100
def gen_noise(z_axis = None):
    if z_axis is None: z_axis = x_y_axis*10

    return noise3array(x_y_axis, x_y_axis, z_axis)[0]

depth_mask = np.zeros(shape=(IMG_DIM_X,IMG_DIM_Y))
for x in range(IMG_DIM_X):
    for y in range(IMG_DIM_Y):
        nx = 2*x/IMG_DIM_X - 1 
        ny = 2*y/IMG_DIM_Y - 1

        depth_mask[x][y] = (1-nx**2) * (1-ny**2)

def gen_img(noise):
    img = Image.new('RGB', (IMG_DIM_X, IMG_DIM_Y), 'white')

    for i, row in enumerate(noise):
        for j, value in enumerate(row):
            d = depth_mask[i][j]
            value = (value+1)/2
            value = int(value * 256 * d)
            if value > 128:
                value = 0
                img.putpixel((i,j), (value, value, value))
                img.putpixel((-i-1,j), (value, value, value))

    return img


root = tk.Tk()
root.geometry(f"{IMG_DIM_X}x{IMG_DIM_Y}")
root.resizable(False, False)

root.update()
imgHeight = (root.winfo_width(), root.winfo_height())

label = tk.Label(root)
label.pack(expand=True, fill="both")

z_axis = np.zeros(1)
def update_img():
    global z_axis
    z_axis += SHIFT_SPEED
    noise = gen_noise(z_axis)
    
    image = gen_img(noise)
    imgTK = ImageTk.PhotoImage(image.resize(imgHeight, resample=Image.NEAREST))
    label.configure(image=imgTK)
    label.update()
    label.after(0, update_img)


label.after(0, update_img)
root.mainloop()