import cv2
import numpy as np
import pickle
import config
"""TODO
        1. Add sys args
        2. Unique color for each class
        3. Write class name on the image when labeling 
"""

classes = ['sedan', 'bus', 'van', 'pickup']
labels={}

def set_curr_class_idx(reset=-1):
    if reset==1:
        config.curr_class_idx = 0
    else:
        config.curr_class_idx +=1

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
        # displaying the coordinates
        # on the image window
        #font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.circle(img, (x,y), radius=3, color=(0, 0, 255), thickness=-1)
        #cv2.putText(img, str(x) + ',' +
        #            str(y), (x,y), font,
        #            1, (255, 0, 0), 2)

        cv2.imshow('image', img)
 
    # checking for right mouse clicks    
    elif event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        set_curr_class_idx()
        if config.curr_class_idx> (len(classes) - 1):
            set_curr_class_idx(1)
        print(f"Switched to the next class...\nPlease check the points corresponding to the {classes[config.curr_class_idx]} class")
        cv2.imshow('image', img)
    else:
        pass
 
if __name__=="__main__": 
    # reading the image
    img = cv2.imread('./images/cars.jpg', 1)
 
    # displaying the image
    cv2.imshow('image', img)
    print(f"Please check the points corresponding to the {classes[config.curr_class_idx]} class")
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()

    with open('./cars.pkl', 'wb') as f:
        pickle.dump(labels, f)