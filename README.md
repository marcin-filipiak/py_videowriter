
# TypingEffectVideo

## Description
This script creates a typing effect by overlaying animated text on a video. The text appears letter by letter, holds for a moment, and then fades out. The application uses OpenCV for video processing and Tkinter for the graphical user interface.

## Requirements
- Python 3
- OpenCV (`cv2`)
- Tkinter (usually comes with Python)

To install the required packages, run:
```sh
pip install opencv-python
````

## How to Use

1. Run the script:

   ```sh
   python script.py
   ```
2. Enter the text you want to animate in the video.
3. Select the font type from the dropdown.
4. Choose the text color.
5. Click "Select Video" and choose an input video file (`.mp4`, `.avi`, `.mov`).
6. Click "Render with Effect" to generate a new video with the typing animation.

After rendering is complete, the output file will be saved as `output.mp4`.

## Features

* Letter-by-letter text animation on top of the video.
* Configurable font and text color.
* Simple and interactive GUI using Tkinter.
* Supports most common video formats.

## Notes

* The animation types one character per video frame.
* The final text holds for 2 seconds and then fades out over 1 second.


