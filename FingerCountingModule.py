import cv2
import time
import os
import HandTrackingModule as htm


class FingerCounter:
    """
    Wraps HandDetector to count how many fingers are raised on one hand.
    Landmark ids used (from MediaPipe hand model):
        4  = thumb tip      8  = index tip
        12 = middle tip      16 = ring tip
        20 = pinky tip
    """

    def __init__(self, detectionCon=0.75, maxHands=1):
        self.detector = htm.HandDetector(detectionCon=detectionCon, maxHands=maxHands)
        self.tipIds = [4, 8, 12, 16, 20]
        self.lmList = []

    def findFingers(self, img, draw=True):
        """Run hand detection on img. Call this once per frame before fingersUp()."""
        img = self.detector.findHands(img, draw=draw)
        self.lmList = self.detector.findPosition(img, draw=False)
        return img

    def fingersUp(self):
        """
        Returns a list of 5 values (1 = up, 0 = down) in order:
        [thumb, index, middle, ring, pinky].
        Returns an empty list if no hand was detected in the last findFingers() call.
        """
        fingers = []
        if len(self.lmList) == 0:
            return fingers

        # Thumb (compares x, since thumb moves sideways not up/down)
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers (compare y: tip above the joint below it = finger up)
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def totalFingers(self):
        """Convenience method: returns the count directly (0-5), or 0 if no hand seen."""
        fingers = self.fingersUp()
        return fingers.count(1) if fingers else 0


def main():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    folderPath = "Fingerimages"
    myList = os.listdir(folderPath)
    overlayList = []
    for imgPath in myList:
        image = cv2.imread(f'{folderPath}/{imgPath}')
        image = cv2.resize(image, (150, 200))
        overlayList.append(image)

    PTime = 0
    counter = FingerCounter(detectionCon=0.75)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = counter.findFingers(img)
        totalFingers = counter.totalFingers()

        if len(counter.lmList) != 0:
            img[0:200, 0:150] = overlayList[totalFingers - 1]

            cv2.rectangle(img, (500, 0), (640, 200), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (530, 150),
                        cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 8)

        cTime = time.time()
        fps = 1 / (cTime - PTime)
        PTime = cTime

        cv2.putText(img, f"FPS: {int(fps)}", (10, 230),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
























# import cv2
# import time 
# import os
# import HandTrackingModule as htm



# wCam, hCam = 640, 480
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)

# folderPath = "Fingerimages"
# myList = os.listdir(folderPath)

# overlayList = []
# for imgPath in myList:
#     image = cv2.imread(f'{folderPath}/{imgPath}')
#     image = cv2.resize(image, (150, 200))
#     overlayList.append(image)

# PTime = 0


# detector = htm.HandDetector(detectionCon=0.75)

# tipIds = [4, 8, 12, 16, 20]

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     img = detector.findHands(img)
#     lmList = detector.findPosition(img, draw=False)

#     if len(lmList) != 0:
#         fingers = []    

#         # Thumb
#         if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
#             fingers.append(1)
#         else:
#             fingers.append(0)

#         # Other fingers
#         for id in range(1,5):

#             if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)


#         totalFingers = fingers.count(1)

#         img[0:200, 0:150] = overlayList[totalFingers-1]

#         # drow rectangle next to image 

#         cv2.rectangle(img, (500, 0), (640, 200), (0, 255, 0), cv2.FILLED)

#         cv2.putText(img, str(totalFingers), (530, 150),
#                     cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 8)

#     cTime = time.time()
#     fps = 1/(cTime-PTime)
#     PTime = cTime

#     cv2.putText(img, f"FPS: {int(fps)}", (10 , 230), cv2.FONT_HERSHEY_PLAIN,2, (255,0,255),2)

    
#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cap.release()
# cv2.destroyAllWindows()