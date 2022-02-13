import pickle

with open('./cars.pkl', 'rb') as f:
    label_obj = pickle.load(f)
    print(type(label_obj))
    print(label_obj)