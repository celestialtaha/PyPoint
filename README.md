# PyPoint

A minimal tool for labeling points and bounding boxes in images using mouse clicks. Supports multiple classes and various save formats.

# Status

✅ Version 1.0 - Functionally Complete

# Features

*   **Point Labeling**: Mark specific points of interest in an image.
*   **Bounding Box Labeling**: Draw bounding boxes around objects.
*   **Multiple Classes**: Define and label multiple object classes.
*   **Switchable Labeling Modes**: Easily switch between 'point' and 'bbox' labeling modes.
*   **Save Label Data**:
    *   **Pickle Format**: Default format for saving labels when moving between images (`n` key).
    *   **MS COCO JSON Format**: Export labels for the current image in COCO format (`j` key).
    *   **Generic JSON Format**: Export labels for the current image in a simple, human-readable JSON format (`k` key).
*   **Load Existing Labels**: Automatically loads and displays saved labels (from `.pkl` files) when an image is displayed.
*   **Image Navigation**:
    *   Move to the next image.
    *   Move to the previous image.
*   **Undo Functionality**: Undo the last labeling action (point, bbox, or bbox start point).
*   **Configurable via Command-Line**:
    *   Specify image directory.
    *   Define class names.
    *   Set workspace directory (for saving session progress).
    *   Set save directory for label files.
*   **Clear Labels**: Option to clear all labels for the current image.
*   **Interactive Status Bar**: Displays current class, mode, and key binding hints.

# Command Line Arguments

PyPoint is configured through command-line arguments:

*   `--dir` (Required): Path to the directory containing the images to be labeled.
    *   Example: `python pypoint.py --dir ./images --classes "['car','person']"`
*   `--classes` (Required): A string representation of a list of class names.
    *   Example: `--classes "['dog','cat','bird']"`
*   `--workspace` (Optional): Specifies a directory to save information about the last labeled item (session progress). Defaults to the current directory (`./`).
    *   Example: `--workspace ./my_pypoint_workspace`
*   `--savedir` (Optional): Specifies a directory where label files (Pickle, COCO JSON, Generic JSON) will be saved. Defaults to the current directory (`./`).
    *   Example: `--savedir ./labels_output`

**Example Usage:**
```bash
python pypoint.py --dir path/to/your/images --classes "['class1','class2','class3']" --savedir ./output_labels
```

# Usage and Key Bindings

The application window displays the image and a status bar with helpful information.

**Mouse Controls:**

*   **Left Mouse Click**:
    *   In 'point' mode: Places a point label for the current class.
    *   In 'bbox' mode:
        *   First click: Sets the first corner of the bounding box.
        *   Second click: Sets the opposite corner and completes the bounding box.
*   **Right Mouse Click**: Switches to the next class in the defined list. If at the last class, it cycles back to the first.
*   **Middle Mouse Click**: Undoes the last action.
    *   If a point or bbox was just added, it's removed.
    *   If the first corner of a bbox was set, it cancels the bbox drawing.

**Keyboard Controls:**

*   **`q`**: Quits the application. Saves the index of the current image, so you can resume later from the same point.
*   **`n`**: Saves the labels for the current image in Pickle format (`.pkl`) and proceeds to the next image. Unsaved labels on the current image are saved before moving.
*   **`p`**: Moves to the previous image. Any unsaved labels on the current image are discarded. Loads labels for the previous image if they exist.
*   **`u`**: Undoes the last action (same as Middle Mouse Click).
*   **`m`**: Switches the labeling mode between 'point' and 'bbox'. The current mode is displayed in the status bar.
*   **`j`**: Saves the labels for the *current image* in MS COCO JSON format (`.coco.json`). This does not advance to the next image.
*   **`k`**: Saves the labels for the *current image* in a generic JSON format (`.generic.json`). This does not advance to the next image.
*   **`r`**: Clears all labels currently drawn or loaded for the *current image*. This action does not automatically save; changes are only persisted via 'n', 'j', or 'k'.
*   **`c`**: (Note: 'c' key was listed in code comments as "Clears the storage?". Its current functionality should be verified. If it's for clearing workspace/session, it should be documented here. If non-functional or for debugging, it might be omitted from user docs.)

**Labeling Process:**

1.  Launch `pypoint.py` with the required arguments.
2.  The first image from the specified directory will be loaded.
3.  Use the mouse and keyboard controls to add, change, and save labels.
4.  The status bar at the bottom of the image will guide you with the current class, mode, and available actions.
5.  Saved label files will appear in the directory specified by `--savedir` (or the current directory if not specified).
