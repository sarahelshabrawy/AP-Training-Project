import sys
import cv2
import numpy as np


class TrackUI:
    angle = 0

    def setup(self):
        def findBestCircle(cnt):
            global angle
            # finds out the best circle according to circularity
            max = 0.8
            maxCnt = cnt[0]
            for c in cnt[0]:
                r = c[2]
                area = 3.14 * r * r
                perimeter = 2 * 3.14 * r
                circularity = 4 * 3.14 * area / (perimeter * perimeter)
                if circularity > max:
                    max = circularity
                    maxCnt = c
            return maxCnt

        detected = False
        boundingBox = (0.0, 0.0, 0.0, 0.0)
        tracker = cv2.TrackerMOSSE_create()
        cap = cv2.VideoCapture(0)
        while True:
            k = cv2.waitKey(1) & 0xFF
            # press 'q' to exit
            if k == ord('q'):
                break
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Blur using 3 * 3 kernel.
            gray_blurred = cv2.GaussianBlur(gray, (5, 5), 250)
            if not ret:
                print("Error opening camera")
                sys.exit()

            if not detected or boundingBox == (0.0, 0.0, 0.0, 0.0):

                # Apply Hough transform on the blurred image.
                detected_circles = cv2.HoughCircles(gray_blurred,
                                                    cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                                    param2=66)

                # Draw circles that are detected.
                if detected_circles is not None:

                    # Convert the circle parameters a, b and r to integers.
                    detected_circles = np.uint16(np.around(detected_circles))
                    pt = findBestCircle(detected_circles)
                    a, b, r = pt[0], pt[1], pt[2]

                    # Draw the circumference of the circle.
                    cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                    boundingBox = (a - r, b - r, 2 * r, 2 * r)
                    p1 = (int(boundingBox[0]), int(boundingBox[1]))
                    p2 = (int(boundingBox[0] + boundingBox[2]), int(boundingBox[1] + boundingBox[3]))
                    cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
                    if detected is False:
                        tracker.init(img, boundingBox)
                    #
                    # # Draw a small circle (of radius 1) to show the center.
                    angle = a
                    cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                    detected = True

                else:
                    cv2.imshow("Detected Circle", img)
                    cv2.waitKey(10)

            ret, boundingBox = tracker.update(gray_blurred)
            if ret:
                # Tracking success
                p1 = (int(boundingBox[0]), int(boundingBox[1]))
                p2 = (int(boundingBox[0] + boundingBox[2]), int(boundingBox[1] + boundingBox[3]))
                cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
                angle = int(boundingBox[0] / 2)
            else:
                # Tracking failure
                cv2.putText(img, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            cv2.imshow("Detected Circle", img)
            cv2.waitKey(90)
            # Display tracker type on frame
        # Convert to grayscale.
