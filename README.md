# ✋ AI Virtual Painter

A real-time, gesture-controlled drawing application that lets you paint on a virtual canvas using nothing but your hand and a webcam — no mouse, no stylus, no touchscreen.

Built with **OpenCV** and **MediaPipe Hands**, the app tracks 21 hand landmarks in real time, classifies which fingers are raised, and maps simple, intuitive gestures to drawing actions.




---

## ✨ Features

- **Hand tracking** using MediaPipe's 21-point hand landmark model
- **Two-mode gesture interaction**:
  - ✌️ **Selection Mode** (index + middle finger up) — pick colors, adjust brush size, or clear the canvas without drawing
  - ☝️ **Drawing Mode** (index finger only) — draw freely on the canvas
- **Color palette** selectable directly from an on-screen header bar
- **Hand-controlled brush/eraser size slider** — no keyboard or mouse needed, just move your finger up and down a vertical slider
- **Eraser tool** built into the same gesture system
- **"Clear All" button**, triggered by hovering over it in Selection Mode
- **Persistent canvas overlay** — strokes stay on screen and blend live with the camera feed using bitwise masking
- **Modular architecture** — hand detection and finger-counting logic are separated into reusable modules (`HandTrackingModule.py`, `FingerCountingModule.py`) that can be reused in other computer vision projects

---

## 🧠 How It Works

1. **Hand Detection** — `HandTrackingModule.py` wraps MediaPipe's `Hands` solution in a simple `HandDetector` class that returns the (x, y) pixel coordinates of all 21 hand landmarks per frame.
2. **Finger Counting** — `FingerCountingModule.py` builds on top of the detector with a `FingerCounter` class that compares landmark positions (e.g. fingertip vs. the joint below it) to determine which of the 5 fingers are raised, returning a list like `[0, 1, 1, 0, 0]`.
3. **Gesture Logic** — the main app (`VirtualPainter.py`) uses the finger state to switch between Selection Mode and Drawing Mode, and maps the index fingertip position to actions: picking a color, adjusting size on the slider, hitting the Clear All button, or drawing a line.
4. **Canvas Compositing** — every stroke is drawn onto a separate NumPy canvas (`imgCanvas`). Each frame, that canvas is masked and merged onto the live camera feed using `cv2.bitwise_and` / `cv2.bitwise_or`, so strokes persist across frames without being erased by new camera input.

---

## 🛠️ Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy

---

## 📦 Installation

```bash
git clone https://github.com/<your-username>/ai-virtual-painter.git
cd ai-virtual-painter
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

pip install -r requirements.txt
```

> **Note:** MediaPipe currently supports Python 3.9–3.12. If you're on Python 3.13, create your virtual environment with an earlier Python version.

**requirements.txt**
```
opencv-python
mediapipe
numpy
```

---

## ▶️ Usage

```bash
python VirtualPainter.py
```

- Show your hand to the webcam.
- Raise **only your index finger** to draw.
- Raise **index + middle fingers** to enter Selection Mode:
  - Move over the header bar to pick a color.
  - Move over the right-side slider to adjust brush/eraser size.
  - Move over the "Clear All" button to reset the canvas.
- Press **`q`** to quit.

---

## 📁 Project Structure

```
ai-virtual-painter/
│
├── HandTrackingModule.py     # Reusable hand-landmark detector class
├── FingerCountingModule.py   # Reusable finger-state (up/down) detector class
├── VirtualPainter.py         # Main application (gesture logic + drawing UI)
├── Header/                   # Color/tool icons shown in the top header bar
├── requirements.txt
└── README.md
```

---

## 🔮 Possible Improvements

- Support for multiple hands / multi-user drawing
- Save/export the canvas as an image (`cv2.imwrite`)
- Undo/redo stroke history
- Shape tools (lines, rectangles, circles) via additional gestures

---

## 📄 License

MIT License — feel free to use, modify, and build on this project.