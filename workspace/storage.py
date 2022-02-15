import pickle
import os

class Storage():
    """
        A class that saves workspace data (the last labeled data info).
    """
    def __init__(self, save_path) -> None:
        self.save_path = save_path
    
    def load(self):
        try:
            with open(os.path.join(self.save_path, 'data.pkl'), 'rb') as f:
                info = pickle.load(f)
                return info
        except:
            print("No previously saved info was found. Or you may want to double check the workspace path. starting from the index 0")
            return [0, ""]

    def save(self, index, file_name):
        with open(os.path.join(self.save_path, 'data.pkl'), 'wb') as f:
            pickle.dump([index, file_name], f)
            print("The last labeled item info was saved. In the next run labeling starts from the last unlabled item.")