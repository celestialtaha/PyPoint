import colorsys
import numpy as np

classes = ['object']
curr_class_idx = 0
dir = './'
save_dir = './'
colors = []
#['sedan', 'bus', 'van', 'pickup']

def set_colors(num_colors=len(classes)):
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        colors.append([r, g, b])