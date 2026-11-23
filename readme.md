# HandScroll

HandScroll is a Python-based hand gesture control project that enables touchless scrolling using a webcam. It uses MediaPipe for real-time hand landmark detection and tracks thumb and index finger movements to recognize pinch gestures. While a pinch is active, vertical hand movement is translated into mouse scroll events.

The project is built with Python, OpenCV, MediaPipe, and PyAutoGUI.

## Features

- Real-time hand tracking using MediaPipe.
- Detection of 21 landmarks per hand.
- Pinch gesture recognition using thumb and index fingertip distance.
- Vertical hand movement tracking while pinching.
- Mouse-wheel scrolling controlled by hand movement.
- Movement smoothing to reduce tracking jitter.
- Configurable scrolling sensitivity and dead zone.
- Webcam-based interaction without additional hardware.

## How It Works

HandScroll processes webcam frames to detect hand landmarks. It uses the distance between the thumb tip and index fingertip to determine whether a pinch gesture is active.

When a pinch is detected, the application tracks the vertical position of the wrist. Changes in wrist position are processed by a scroll controller, which applies smoothing and converts hand movement into mouse-wheel events.

The interaction follows this sequence:

1. The webcam captures a video frame.
2. MediaPipe detects the hand and its landmarks.
3. The gesture recognizer checks for a pinch.
4. The movement tracker measures vertical wrist displacement.
5. The scroll controller processes the movement and generates scroll events.

Scrolling stops when the pinch is released.

## Technology Stack

- **Python** – Core programming language.
- **MediaPipe** – Hand landmark detection and tracking.
- **OpenCV** – Webcam access and image processing.
- **PyAutoGUI** – Mouse-wheel event simulation.
- **Flask** – Web application framework for the project interface.

## Requirements

- Python 3.10 or later.
- A webcam.
- Linux with an X11 desktop session for the current PyAutoGUI scrolling implementation.
- Git.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/prbn-ach/HandScroll.git
cd HandScroll
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

Install the required Python packages using the requirements file:

```bash
pip install -r requirements.txt
```


## Usage

Run:

```bash
python app.py
```

Open a webpage or document with enough content to scroll.

- Pinch to activate scrolling.
- Move your hand upward to scroll upward.
- Move your hand downward to scroll downward.
- Release the pinch to stop scrolling.

Press `q` on webcam window to exit.

## Configuration

Scrolling behavior can be adjusted in `app.py` through the `ScrollController` parameters.

```python
scroll_controller = ScrollController(
    sensitivity=0.025,
    smoothing=0.55,
    dead_zone=0.8,
    max_delta=35
)
```

| Parameter | Description |
|---|---|
| `sensitivity` | Controls the scrolling speed. |
| `smoothing` | Controls how quickly the controller responds to movement changes. |
| `dead_zone` | Ignores very small movements to reduce unwanted scrolling. |
| `max_delta` | Limits the maximum movement processed per frame. |

Adjust these values according to your webcam and preferred scrolling behavior.

## Platform Compatibility

The current scrolling implementation uses PyAutoGUI to generate mouse-wheel events.

On Linux, PyAutoGUI's desktop interaction generally requires an X11 session. Wayland environments may require additional configuration or a different input-control implementation.

The application also requires webcam access and appropriate camera permissions.

## Troubleshooting

**Webcam is not detected**

- Check whether the webcam is connected.
- Ensure other applications are not using the camera.
- Verify the camera index in `cv2.VideoCapture(0)`.

**Hand landmarks are not detected**

- Ensure your hand is visible and adequately illuminated.
- Keep your hand within the webcam's field of view.
- Avoid excessive motion blur.

**Pinch gesture is not recognized reliably**

- Adjust `pinch_start` and `pinch_release` in `GestureRecognizer`.
- Ensure both fingertips are visible to the camera.

**Scrolling is too fast or too slow**

- Adjust the `sensitivity` parameter in `ScrollController`.

**Scrolling feels delayed or unstable**

- Adjust the `smoothing` and `dead_zone` parameters.
- Ensure the webcam is providing a consistent frame rate.

## Development Status

The core hand tracking, pinch recognition, movement tracking, and mouse scrolling components are implemented.

Further development can focus on integrating these components into the Flask interface, improving application controls, and refining the overall user experience.

## Acknowledgements

- [MediaPipe](https://github.com/google-ai-edge/mediapipe) for hand landmark detection and tracking.
- [OpenCV](https://github.com/opencv/opencv) for computer vision and webcam access.
- [PyAutoGUI](https://github.com/asweigart/pyautogui) for mouse and keyboard automation.