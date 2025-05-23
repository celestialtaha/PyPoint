import colorsys
import numpy as np

classes = ['object']
curr_class_idx = 0
dir = './'
save_dir = './'
colors = []
#['sedan', 'bus', 'van', 'pickup']

stat_height = 100
last_image_cache = None
img_stat= None
undo = False
curr_labels = {}

# Labeling mode: 'point' or 'bbox'
labeling_mode = 'point'
# For bbox drawing: stores the (x,y) of the first click
bbox_start_point = None

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