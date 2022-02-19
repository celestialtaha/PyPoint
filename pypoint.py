from workspace import storage
import argparse
import numpy as np
import cv2
import os
import pickle
import config

"""TODO
        1. Add previous button
        2. Load labels from saved data on displayed image
        3. Add b.b labeling feature
        4. Add MS COCO Saving format
        5. Add save as json
"""

# ----------------- Define cml arguments ---------------------- #
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, required=True, default='single', help='The path to the file in which the images exist.')
parser.add_argument('--classes',type=str, required=True, help='The name of the classes to be labeled. A list of str.')
parser.add_argument('--workspace',type=str, required=False, default='./', help='Specifies a directory to save the last labeled item info.')
parser.add_argument('--savedir',type=str, required=False, default='./', help='Specifies a directory to save the labeled data.')

# ------------- Parse cml arguments and set config ------------------ #
args = parser.parse_args()
config.dir = args.dir
config.save_dir = args.savedir
config.workspace = args.workspace
config.classes = args.classes.strip('[]').split(',')
config.set_colors(len(config.classes))

def update_stat():
    """
        Updates the status bar context
    """
    config.img_stat[img.shape[0]:, :,:] = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(config.img_stat,f"Labeling {config.classes[config.curr_class_idx]}", (10, img.shape[0]+30), font, 1, (255,255,255),2)
    cv2.putText(config.img_stat,f"Guide: q: save&exit / u: undo / leftMouse: Place label / rightMouse: Next class", (10, img.shape[0]+60), font, 0.5, (255,255,255),1)
    print(f"Switched to the next class...\nPlease check the points corresponding to the {config.classes[config.curr_class_idx]} class")


def click_event(event, x, y, flags, params):
    """
        Handles the mouse click event
    """
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        
        if config.undo:
            config.undo = False
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        try:
            config.curr_labels[config.classes[config.curr_class_idx]].append((x,y))
        except:
            config.curr_labels[config.classes[config.curr_class_idx]] = [(x,y)]
        
        # displaying the dot
        config.last_image_cache = config.img_stat.copy()
        config.img_stat = cv2.circle(config.img_stat, (x,y), radius=4, color=config.colors[config.curr_class_idx], thickness=-1)

        cv2.imshow('image', config.img_stat)
 
    # checking for right mouse clicks    
    elif event==cv2.EVENT_RBUTTONDOWN:
        if config.undo:
            config.undo = False
        # displaying the coordinates
        # on the Shell
        set_curr_class_idx()
        if config.curr_class_idx> (len(config.classes) - 1):
            set_curr_class_idx(1)
        
        update_stat()
        cv2.imshow('image', config.img_stat)

    elif event== cv2.EVENT_MBUTTONDOWN:
        # undo operation
        try:
            if not config.undo:
                config.curr_labels[config.classes[config.curr_class_idx]].pop()
                config.img_stat = config.last_image_cache
                cv2.imshow('image', config.img_stat)
                config.undo = True
            else:
                print("Only one step undo is supported. You can restart labeling process for this smaple with the 'r' key.")
        except:
            pass
        
    else:
        pass

def set_curr_class_idx(reset=-1):
    if reset==1:
        config.curr_class_idx = 0
    else:
        config.curr_class_idx +=1

if __name__=="__main__":

    strg = storage.Storage('./workspace/')
    last_idx, last_fname = [0, ""]
    last_idx, last_fname = strg.load()
    files = os.listdir(config.dir)
    i = 0

    while i < len(files):
        if last_idx>0:
            if i<=last_idx:
                i+=1
                continue
        # read the image
        img = cv2.imread(os.path.join(config.dir, files[i]), 1)
        config.img_stat = np.zeros((img.shape[0]+config.stat_height, img.shape[1], img.shape[2]), dtype=img.dtype)
        config.img_stat[:img.shape[0],:img.shape[1],:] = img

        # display the image
        update_stat()
        cv2.imshow('image', config.img_stat)    

        # Set mouse click event handler
        cv2.setMouseCallback('image', click_event)

        # listen for keys
        key = cv2.waitKey(0)
        if key == ord('q'):
            #Exit
            #storage.save(i, file)
            break
        elif key == ord('n'):
            # Save and proceed to the next file
            with open(os.path.join(config.save_dir, f'./{files[i]}.pkl'), 'wb') as f:
                pickle.dump(config.curr_labels, f)
                print(f"The label for {files[i]} was succesfully saved!")
                set_curr_class_idx(1)
            strg.save(i, files[i])
            config.curr_labels = {}
            i+=1

        elif key== ord('c'):
            # Clears the storage?
            pass
        elif key==ord('r'):
            config.curr_labels = {}


    # close the window
    cv2.destroyAllWindows()