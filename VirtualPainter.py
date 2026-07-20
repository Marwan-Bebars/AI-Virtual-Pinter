import cv2
import numpy as np
import os
import FingerCountingModule as fcm
# --------------------------------------------------

# -----------------load Images-----------------
folderPath = "./Header"
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

# -----------------Drawing Setting-----------------
drawColor = (255, 0, 255)
brushThickness = 15
eraserThickness = 50
xp, yp = 0, 0

MIN_SIZE, MAX_SIZE = 5, 60

# -----------------Size slider panel geometry-----------------
sliderX1, sliderX2 = 1190, 1250     # slider track left/right
sliderY1, sliderY2 = 175, 575       # slider track top/bottom (top = max size), shifted down 15px

clearBtnX1, clearBtnX2 = 1150, 1270   # top-right "Clear All" button
clearBtnY1, clearBtnY2 = 130, 168


def sizeToY(size):
    """Convert a brush size to the handle's y position on the slider."""
    ratio = (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE)
    return int(sliderY2 - ratio * (sliderY2 - sliderY1))


def yToSize(y):
    """Convert a y position on the slider to a brush size."""
    y = max(sliderY1, min(sliderY2, y))
    ratio = (sliderY2 - y) / (sliderY2 - sliderY1)
    return int(MIN_SIZE + ratio * (MAX_SIZE - MIN_SIZE))


def drawPanel(img, pt1, pt2, color=(30, 30, 30), alpha=0.55, border_color=(200, 200, 200)):
    """Semi-transparent rounded-feel panel with a thin border."""
    overlay = img.copy()
    cv2.rectangle(overlay, pt1, pt2, color, cv2.FILLED)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    cv2.rectangle(img, pt1, pt2, border_color, 1, cv2.LINE_AA)


def drawSlider(img, currentSize, activeColor):
    drawPanel(img, (sliderX1 - 10, sliderY1 - 40), (sliderX2 + 10, sliderY2 + 45))

    # track
    cv2.rectangle(img, (sliderX1, sliderY1), (sliderX2, sliderY2), (80, 80, 80), cv2.FILLED, cv2.LINE_AA)

    # filled portion (from the bottom up to the current size)
    handleY = sizeToY(currentSize)
    cv2.rectangle(img, (sliderX1, handleY), (sliderX2, sliderY2), activeColor, cv2.FILLED, cv2.LINE_AA)

    # handle
    cx = (sliderX1 + sliderX2) // 2
    cv2.circle(img, (cx, handleY), 14, (255, 255, 255), cv2.FILLED, cv2.LINE_AA)
    cv2.circle(img, (cx, handleY), 14, activeColor, 2, cv2.LINE_AA)

    # label + live size number
    cv2.putText(img, "SIZE", (sliderX1 - 2, sliderY1 - 15), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, str(currentSize), (sliderX1 + 5, sliderY2 + 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 255), 2, cv2.LINE_AA)


def drawClearButton(img):
    cv2.rectangle(img, (clearBtnX1, clearBtnY1), (clearBtnX2, clearBtnY2), (0, 0, 200), cv2.FILLED, cv2.LINE_AA)
    cv2.rectangle(img, (clearBtnX1, clearBtnY1), (clearBtnX2, clearBtnY2), (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img, "Clear All", (clearBtnX1 + 8, clearBtnY1 + 26), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 2, cv2.LINE_AA)


def pointInBox(x, y, pt1, pt2):
    return pt1[0] < x < pt2[0] and pt1[1] < y < pt2[1]


# -----------------Webcam-----------------
header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

counter = fcm.FingerCounter(detectionCon=0.85)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import Image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmark
    img = counter.findFingers(img)
    lmList = counter.lmList

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]    # index finger tip
        x2, y2 = lmList[12][1:]   # middle finger tip

        # 3. Check which fingers are up
        fingers = counter.fingersUp()

        # 4. Selection mode - index AND middle fingers up
        if fingers[1] == True and fingers[2] == True:
            xp, yp = 0, 0

            # -- color selection from the top header --
            if y1 < 125:
                if 250 < x1 < 400:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 450 < x1 < 600:
                    header = overlayList[1]
                    drawColor = (255, 144, 30)  
                elif 700 < x1 < 850:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1000 < x1 < 1150:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            # -- brush/eraser size from the side slider --
            if pointInBox(x1, y1, (sliderX1, sliderY1), (sliderX2, sliderY2)):
                newSize = yToSize(y1)
                if drawColor == (0, 0, 0):
                    eraserThickness = newSize
                else:
                    brushThickness = newSize

            # -- clear all --
            if pointInBox(x1, y1, (clearBtnX1, clearBtnY1), (clearBtnX2, clearBtnY2)):
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)

            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 30), drawColor, cv2.FILLED, cv2.LINE_AA)

        # 5. Drawing mode - only index finger up
        elif fingers[1] == True and fingers[2] == False:
            currentThickness = eraserThickness if drawColor == (0, 0, 0) else brushThickness
            cv2.circle(img, (x1, y1), currentThickness // 2, drawColor, cv2.FILLED, cv2.LINE_AA)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, currentThickness, cv2.LINE_AA)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, currentThickness, cv2.LINE_AA)
            xp, yp = x1, y1

        else:
            xp, yp = 0, 0
    else:
        xp, yp = 0, 0

    # merge the canvas onto the live feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # header bar
    img[0:125, 0:1280] = header

    # size/clear panel (drawn on top, always visible)
    activeSize = eraserThickness if drawColor == (0, 0, 0) else brushThickness
    activeColor = (255, 255, 255) if drawColor == (0, 0, 0) else drawColor
    drawSlider(img, activeSize, activeColor)
    drawClearButton(img)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()