import cv2
import numpy as np
import pickle
import config
"""TODO
        1. Add sys args
        2. Unique color for each class
        3. Add MS COCO Saving format
        4. Add save as json
        5. Add b.b labeling feature
        6. Add directory mode and single mode labeling (sys-arg)
"""

classes = ['sedan', 'bus', 'van', 'pickup']
labels={}

def set_curr_class_idx(reset=-1):
    if reset==1:
        config.curr_class_idx = 0
    else:
        config.curr_class_idx +=1

def update_stat():
    img_stat[img.shape[0]:, :,:] = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_stat,f"Labeling {classes[config.curr_class_idx]}", (10, img.shape[0]+30), font, 1, (255,255,255),2)
    cv2.putText(img_stat,f"Guide: q: save&exit / u: undo / leftMouse: Place label / rightMouse: Next class", (10, img.shape[0]+60), font, 0.5, (255,255,255),1)
    print(f"Switched to the next class...\nPlease check the points corresponding to the {classes[config.curr_class_idx]} class")

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        try:
            labels[classes[config.curr_class_idx]].append((x,y))
        except:
            labels[classes[config.curr_class_idx]] = [(x,y)]
        
        # displaying the dot
        image = cv2.circle(img_stat, (x,y), radius=3, color=(0, 0, 255), thickness=-1)

        cv2.imshow('image', img_stat)
 
    # checking for right mouse clicks    
    elif event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        set_curr_class_idx()
        if config.curr_class_idx> (len(classes) - 1):
            set_curr_class_idx(1)
        
        update_stat()
        cv2.imshow('image', img_stat)
    else:
        pass
 
if __name__=="__main__": 
    # reading the image
    img = cv2.imread('./images/cars.jpg', 1)
    img_stat = np.zeros((img.shape[0]+100, img.shape[1], img.shape[2]),dtype=img.dtype)
    img_stat[:img.shape[0],:img.shape[1],:] = img
 
    # displaying the image
    update_stat()
    cv2.imshow('image', img_stat)    
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()

    with open('./cars.pkl', 'wb') as f:
        pickle.dump(labels, f)
        print("The label was succesfully saved!")