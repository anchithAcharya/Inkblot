from glob import escape
import tkinter as tk
import numpy as np
from opensimplex import noise3array, random_seed
from PIL import Image, ImageTk


IMG_DIM_X = 1000
IMG_DIM_Y = 500
SHIFT_SPEED = 0.05
THRESHOLD_MASK = True
THRESHOLD_VALUE = 128
PAUSE = False
SCROLL_CTRL = True
QUIT = False

random_seed()
x_y_axis = np.arange(0,IMG_DIM_X/2)/75
def gen_noise(z_axis = None):
    if z_axis is None: z_axis = x_y_axis*10

    return noise3array(x_y_axis, x_y_axis, z_axis)[0]

depth_mask = np.zeros(shape=(IMG_DIM_X,IMG_DIM_Y))
for x in range(IMG_DIM_X):
    for y in range(IMG_DIM_Y):
        nx = 2*x/IMG_DIM_X - 1 
        ny = 2*y/IMG_DIM_Y - 1

        depth_mask[x][y] = (1-nx**2) * (1-ny**2)

TOP = 0
BOTTOM = 1
PULL = 50

def contrast(num):
    delta = num * (PULL/100)

    if num > (TOP + BOTTOM)/2:
        return delta
    
    else:
        return BOTTOM - delta

def gen_img(noise):
    img = Image.new('RGB', (IMG_DIM_X, IMG_DIM_Y), 'white')

    for i, row in enumerate(noise):
        for j, value in enumerate(row):
            d = depth_mask[i][j]
            value = (value+1)/2
            value = contrast(value)
            value = int(value * 256 * d)


            threshold = THRESHOLD_VALUE if THRESHOLD_MASK else 0
            if value > threshold:
                if THRESHOLD_MASK: value = 0
                img.putpixel((i,j), (value, value, value))
                img.putpixel((-i-1,j), (value, value, value))

    return img

def click_func(_):
    global THRESHOLD_MASK
    THRESHOLD_MASK = not THRESHOLD_MASK

def pause(_):
    global PAUSE
    PAUSE = not PAUSE

def escape(_):
    global QUIT
    QUIT = not QUIT

def scroll_ctrl(_):
    global SCROLL_CTRL
    SCROLL_CTRL = not SCROLL_CTRL

def change_threshold(e):
    global THRESHOLD_VALUE, PULL

    if SCROLL_CTRL: THRESHOLD_VALUE -= (e.delta / 120)
    else:
        PULL -= (e.delta / 120)
        if PULL > 100: PULL = 100
        if PULL < 0: PULL = 0

def main():
	def update_img():
		nonlocal z_axis
		if not PAUSE: z_axis += SHIFT_SPEED
		
		imgTK = ImageTk.PhotoImage(gen_img(gen_noise(z_axis)))
		label.configure(image=imgTK)
		label.update()
		
		if QUIT: root.quit()
		else: label.after(0, update_img)

	root = tk.Tk()
	root.geometry(f"{IMG_DIM_X}x{IMG_DIM_Y}")
	root.resizable(False, False)

	root.update()

	label = tk.Label(root)
	label.pack(expand=True, fill="both")
	label.bind("<Button-1>", click_func)
	label.bind("<Button-2>", scroll_ctrl)
	label.focus_set()
	label.bind("<space>", pause)
	label.bind("<Escape>", escape)
	label.bind("<MouseWheel>", lambda e: change_threshold(e))

	z_axis = np.zeros(1)

	label.after(0, update_img)
	root.mainloop()

import cProfile
cProfile.runctx('main()', globals=globals(), locals=locals(), filename="output.dat")

import pstats
with open('output_time.txt', 'w') as f:
	p = pstats.Stats('output.dat', stream=f)
	p.sort_stats('time').print_stats()