from workspace import storage
import argparse
import numpy as np
import cv2
import os
import pickle
import config

"""TODO
        1. Add b.b labeling feature
        2. Add MS COCO Saving format
        3. Add save as json
"""

labels={}

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
    img_stat[img.shape[0]:, :,:] = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_stat,f"Labeling {config.classes[config.curr_class_idx]}", (10, img.shape[0]+30), font, 1, (255,255,255),2)
    cv2.putText(img_stat,f"Guide: q: save&exit / u: undo / leftMouse: Place label / rightMouse: Next class", (10, img.shape[0]+60), font, 0.5, (255,255,255),1)
    print(f"Switched to the next class...\nPlease check the points corresponding to the {config.classes[config.curr_class_idx]} class")


def click_event(event, x, y, flags, params):
    """
        Handles the mouse click event
    """
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        try:
            labels[config.classes[config.curr_class_idx]].append((x,y))
        except:
            labels[config.classes[config.curr_class_idx]] = [(x,y)]
        
        # displaying the dot
        image = cv2.circle(img_stat, (x,y), radius=4, color=config.colors[config.curr_class_idx], thickness=-1)

        cv2.imshow('image', img_stat)
 
    # checking for right mouse clicks    
    elif event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        set_curr_class_idx()
        if config.curr_class_idx> (len(config.classes) - 1):
            set_curr_class_idx(1)
        
        update_stat()
        cv2.imshow('image', img_stat)
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

    for i,file in enumerate(os.listdir(config.dir)):
        if last_idx>0:
            if i<=last_idx:
                continue
        # read the image
        img = cv2.imread(os.path.join(config.dir, file), 1)
        img_stat = np.zeros((img.shape[0]+100, img.shape[1], img.shape[2]), dtype=img.dtype)
        img_stat[:img.shape[0],:img.shape[1],:] = img

        # display the image
        update_stat()
        cv2.imshow('image', img_stat)    

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
            with open(os.path.join(config.save_dir, f'./{file}.pkl'), 'wb') as f:
                pickle.dump(labels, f)
                print(f"The label for {file} was succesfully saved!")
                set_curr_class_idx(1)
            strg.save(i, file)
        elif key== ord('c'):
            # Clears the storage?
            pass

    # close the window
    cv2.destroyAllWindows()