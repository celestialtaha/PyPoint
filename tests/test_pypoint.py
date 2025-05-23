import unittest
import os
import shutil
import pickle
import json
import numpy as np
import cv2

# Attempt to import application modules
# This might require adjusting PYTHONPATH or the project structure if pypoint is not directly importable
# For now, assuming pypoint.py and config.py are in the parent directory or accessible
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pypoint
import config

class TestPyPoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(__file__)
        cls.dummy_images_dir = os.path.join(cls.base_dir, "dummy_images")
        cls.dummy_labels_dir = os.path.join(cls.base_dir, "dummy_labels")
        cls.dummy_workspace_dir = os.path.join(cls.base_dir, "dummy_workspace")

        # Create dummy directories
        os.makedirs(cls.dummy_images_dir, exist_ok=True)
        os.makedirs(cls.dummy_labels_dir, exist_ok=True)
        os.makedirs(cls.dummy_workspace_dir, exist_ok=True)

        # Create dummy image files
        cls.dummy_image_names = ["img1.jpg", "img2.png"]
        cls.dummy_image_paths = []
        for img_name in cls.dummy_image_names:
            path = os.path.join(cls.dummy_images_dir, img_name)
            # Create a small blank image (100x100, 3 channels, white)
            dummy_img = np.full((100, 100, 3), 255, dtype=np.uint8)
            cv2.imwrite(path, dummy_img)
            cls.dummy_image_paths.append(path)
        
        # Setup config for testing
        config.dir = cls.dummy_images_dir
        config.save_dir = cls.dummy_labels_dir
        config.workspace = cls.dummy_workspace_dir
        config.classes = ['test_obj1', 'test_obj2']
        config.set_colors(len(config.classes)) # Initialize colors
        config.curr_labels = {}
        config.labeling_mode = 'point'
        config.bbox_start_point = None
        config.curr_class_idx = 0
        
        # Mock parts of pypoint that interact with OpenCV GUI directly if needed
        # For now, we'll try to test data functions first.
        # pypoint.img = dummy_img # Mock the global 'img' if functions directly use it
        # pypoint.files = cls.dummy_image_names # Mock global 'files'
        # pypoint.i = 0 # Mock global 'i'

    @classmethod
    def tearDownClass(cls):
        # Remove temporary directories
        shutil.rmtree(cls.dummy_images_dir)
        shutil.rmtree(cls.dummy_labels_dir)
        shutil.rmtree(cls.dummy_workspace_dir)

    def setUp(self):
        # Reset curr_labels before each test
        config.curr_labels = {}
        config.curr_class_idx = 0
        config.labeling_mode = 'point'
        config.bbox_start_point = None
        # Ensure dummy files/dirs exist if any test accidentally removes them individually
        os.makedirs(self.dummy_images_dir, exist_ok=True)
        os.makedirs(self.dummy_labels_dir, exist_ok=True)
        os.makedirs(self.dummy_workspace_dir, exist_ok=True)


    def test_initial_setup_correct(self):
        self.assertTrue(os.path.exists(self.dummy_images_dir))
        self.assertTrue(os.path.exists(self.dummy_labels_dir))
        self.assertTrue(os.path.exists(self.dummy_workspace_dir))
        self.assertEqual(len(os.listdir(self.dummy_images_dir)), len(self.dummy_image_names))
        self.assertEqual(config.dir, self.dummy_images_dir)
        self.assertEqual(config.save_dir, self.dummy_labels_dir)

    def test_pickle_save_and_load_labels(self):
        # 1. Simulate adding labels
        image_filename = self.dummy_image_names[0]
        config.curr_labels = {
            'test_obj1': [
                {'type': 'point', 'coords': (10, 20)},
                {'type': 'point', 'coords': (15, 25)}
            ],
            'test_obj2': [
                {'type': 'bbox', 'coords': (30, 40, 50, 60)} # x1, y1, x2, y2
            ]
        }
        original_labels = config.curr_labels.copy() # Deep copy if necessary, but dict of lists of dicts is fine here

        # 2. Simulate saving (directly using pickle as pypoint.py would for 'n' key)
        pickle_file_path = os.path.join(config.save_dir, f'{image_filename}.pkl')
        with open(pickle_file_path, 'wb') as f:
            pickle.dump(config.curr_labels, f)
        
        self.assertTrue(os.path.exists(pickle_file_path))

        # 3. Clear current labels
        config.curr_labels = {}

        # 4. Simulate loading
        # The actual pypoint code loads into config.curr_labels, so we'll mimic that.
        # The drawing part is visual, so we test if data is loaded correctly.
        if os.path.exists(pickle_file_path):
            try:
                with open(pickle_file_path, 'rb') as f:
                    loaded_labels = pickle.load(f)
                    config.curr_labels = loaded_labels
            except Exception as e:
                self.fail(f"Pickle loading failed: {e}")
        
        # 5. Assert that loaded labels match original
        self.assertEqual(config.curr_labels, original_labels)
        self.assertIn('test_obj1', config.curr_labels)
        self.assertEqual(len(config.curr_labels['test_obj1']), 2)
        self.assertEqual(config.curr_labels['test_obj1'][0]['coords'], (10, 20))
        self.assertIn('test_obj2', config.curr_labels)
        self.assertEqual(config.curr_labels['test_obj2'][0]['type'], 'bbox')
        self.assertEqual(config.curr_labels['test_obj2'][0]['coords'], (30, 40, 50, 60))

    def test_generic_json_saving(self):
        image_filename = self.dummy_image_names[0]
        image_shape = (100, 100, 3) # height, width, channels - matching setUpClass dummy image

        config.curr_labels = {
            'test_obj1': [
                {'type': 'point', 'coords': (5, 15)},
            ],
            'test_obj2': [
                {'type': 'bbox', 'coords': (25, 35, 45, 55)}
            ]
        }
        expected_labels_data = config.curr_labels.copy()

        # Call the save_generic_json function from pypoint
        pypoint.save_generic_json(image_filename, image_shape, config.curr_labels, config.save_dir)

        # Verify the file was created
        base_filename, _ = os.path.splitext(image_filename)
        json_file_path = os.path.join(config.save_dir, f'{base_filename}.generic.json')
        self.assertTrue(os.path.exists(json_file_path))

        # Load the JSON file and parse its content
        with open(json_file_path, 'r') as f:
            saved_data = json.load(f)
        
        # Assertions
        self.assertEqual(saved_data['image_filename'], image_filename)
        self.assertEqual(saved_data['image_dimensions']['width'], image_shape[1])
        self.assertEqual(saved_data['image_dimensions']['height'], image_shape[0])
        self.assertEqual(saved_data['labels'], expected_labels_data)
        self.assertIn('test_obj1', saved_data['labels'])
        self.assertEqual(saved_data['labels']['test_obj1'][0]['coords'], [5, 15]) # JSON lists, not tuples
        self.assertIn('test_obj2', saved_data['labels'])
        self.assertEqual(saved_data['labels']['test_obj2'][0]['coords'], [25, 35, 45, 55])

    def test_coco_json_saving(self):
        image_filename = self.dummy_image_names[1] # Use the second dummy image
        image_shape = (100, 100, 3) # height, width, channels

        config.curr_labels = {
            'test_obj1': [ # Class 'test_obj1' is at index 0 in config.classes
                {'type': 'point', 'coords': (50, 60)},
            ],
            'test_obj2': [ # Class 'test_obj2' is at index 1 in config.classes
                {'type': 'bbox', 'coords': (10, 10, 40, 50)} # x1, y1, x2, y2
            ]
        }
        
        # Call the save_coco_format function from pypoint
        pypoint.save_coco_format(image_filename, image_shape, config.curr_labels, config.classes, config.save_dir)

        # Verify the file was created
        base_filename, _ = os.path.splitext(image_filename)
        coco_file_path = os.path.join(config.save_dir, f'{base_filename}.coco.json')
        self.assertTrue(os.path.exists(coco_file_path))

        # Load the COCO JSON file and parse its content
        with open(coco_file_path, 'r') as f:
            coco_data = json.load(f)

        # Assertions
        # Info and Licenses (minimal check)
        self.assertIn('info', coco_data)
        self.assertIn('licenses', coco_data)

        # Images
        self.assertIn('images', coco_data)
        self.assertEqual(len(coco_data['images']), 1)
        coco_image = coco_data['images'][0]
        self.assertEqual(coco_image['file_name'], image_filename)
        self.assertEqual(coco_image['width'], image_shape[1])
        self.assertEqual(coco_image['height'], image_shape[0])
        self.assertEqual(coco_image['id'], 0) # As per current save_coco_format logic

        # Categories
        self.assertIn('categories', coco_data)
        self.assertEqual(len(coco_data['categories']), len(config.classes))
        for i, class_name in enumerate(config.classes):
            self.assertEqual(coco_data['categories'][i]['name'], class_name)
            self.assertEqual(coco_data['categories'][i]['id'], i) # ID should be index

        # Annotations
        self.assertIn('annotations', coco_data)
        self.assertEqual(len(coco_data['annotations']), 2) # One point, one bbox

        # Point annotation checks (for test_obj1, category_id 0)
        point_ann = next(ann for ann in coco_data['annotations'] if ann['category_id'] == 0)
        self.assertIsNotNone(point_ann)
        self.assertEqual(point_ann['image_id'], 0)
        self.assertEqual(point_ann['segmentation'], [[50.0, 60.0]])
        self.assertEqual(point_ann['bbox'], [50.0, 60.0, 1.0, 1.0])
        self.assertEqual(point_ann['area'], 1.0)
        self.assertEqual(point_ann['iscrowd'], 0)

        # Bbox annotation checks (for test_obj2, category_id 1)
        bbox_ann = next(ann for ann in coco_data['annotations'] if ann['category_id'] == 1)
        self.assertIsNotNone(bbox_ann)
        self.assertEqual(bbox_ann['image_id'], 0)
        x1, y1, x2, y2 = 10.0, 10.0, 40.0, 50.0
        width, height = x2 - x1, y2 - y1
        self.assertEqual(bbox_ann['bbox'], [x1, y1, width, height])
        self.assertEqual(bbox_ann['segmentation'], [[x1, y1, x1, y2, x2, y2, x2, y1]])
        self.assertEqual(bbox_ann['area'], width * height)
        self.assertEqual(bbox_ann['iscrowd'], 0)

    def test_bbox_coordinate_normalization(self):
        # Set mode to bbox and select a class
        config.labeling_mode = 'bbox'
        config.curr_class_idx = 0 # 'test_obj1'
        current_class_name = config.classes[config.curr_class_idx]

        # Mock image for click_event (not strictly necessary as click_event doesn't use img directly for coord logic)
        # pypoint.img_stat = np.zeros((100,100,3), dtype=np.uint8) # If drawing was tested

        # Case 1: x1 > x2, y1 < y2
        config.bbox_start_point = None
        config.curr_labels = {} # Reset labels
        # First click
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 70, 10, None, None) 
        self.assertEqual(config.bbox_start_point, (70, 10))
        # Second click
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 20, 80, None, None) 
        
        self.assertIn(current_class_name, config.curr_labels)
        self.assertEqual(len(config.curr_labels[current_class_name]), 1)
        label_item = config.curr_labels[current_class_name][0]
        self.assertEqual(label_item['type'], 'bbox')
        # Expected: (20, 10, 70, 80)
        self.assertEqual(label_item['coords'], (20, 10, 70, 80))
        self.assertIsNone(config.bbox_start_point) # Should be reset

        # Case 2: x1 < x2, y1 > y2
        config.bbox_start_point = None
        config.curr_labels = {} # Reset labels
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 10, 80, None, None)
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 70, 20, None, None)
        
        self.assertIn(current_class_name, config.curr_labels)
        self.assertEqual(len(config.curr_labels[current_class_name]), 1)
        label_item = config.curr_labels[current_class_name][0]
        # Expected: (10, 20, 70, 80)
        self.assertEqual(label_item['coords'], (10, 20, 70, 80))

        # Case 3: x1 > x2, y1 > y2
        config.bbox_start_point = None
        config.curr_labels = {} # Reset labels
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 70, 80, None, None)
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 10, 20, None, None)
        
        self.assertIn(current_class_name, config.curr_labels)
        self.assertEqual(len(config.curr_labels[current_class_name]), 1)
        label_item = config.curr_labels[current_class_name][0]
        # Expected: (10, 20, 70, 80)
        self.assertEqual(label_item['coords'], (10, 20, 70, 80))

        # Case 4: Normal order (x1 < x2, y1 < y2) - just to be sure
        config.bbox_start_point = None
        config.curr_labels = {} # Reset labels
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 10, 20, None, None)
        pypoint.click_event(cv2.EVENT_LBUTTONDOWN, 70, 80, None, None)
        
        self.assertIn(current_class_name, config.curr_labels)
        self.assertEqual(len(config.curr_labels[current_class_name]), 1)
        label_item = config.curr_labels[current_class_name][0]
        # Expected: (10, 20, 70, 80)
        self.assertEqual(label_item['coords'], (10, 20, 70, 80))

    def test_previous_image_action(self):
        # Simulate being on the second image (index 1)
        current_image_index = 1
        
        # Simulate some labels being present for the "current" image before going previous
        config.curr_labels = {'test_obj1': [{'type': 'point', 'coords': (1, 1)}]}
        config.bbox_start_point = (5,5) # Simulate an incomplete bbox
        config.curr_class_idx = 1 # Simulate being on the second class

        # Call the refactored function
        new_image_index = pypoint.process_previous_action(current_image_index)

        # Assertions for state changes
        self.assertEqual(new_image_index, 0, "Image index should decrement to 0")
        self.assertEqual(config.curr_labels, {}, "curr_labels should be cleared")
        self.assertIsNone(config.bbox_start_point, "bbox_start_point should be reset")
        self.assertEqual(config.curr_class_idx, 0, "curr_class_idx should be reset to 0 by set_curr_class_idx(1)")

        # Simulate being on the first image (index 0)
        current_image_index = 0
        config.curr_labels = {'test_obj1': [{'type': 'point', 'coords': (2, 2)}]} # Add some labels again
        
        new_image_index = pypoint.process_previous_action(current_image_index)
        
        self.assertEqual(new_image_index, 0, "Image index should remain 0 if already at the start")
        self.assertEqual(config.curr_labels, {}, "curr_labels should be cleared even if at index 0")


if __name__ == "__main__":
    unittest.main()
