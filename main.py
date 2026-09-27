import cv2
import time

from detector import ObjectDetector
from hud import XenoHUD
from hand_tracker import HandTracker
from effects import EnergyEffects


WINDOW_NAME = "XENO-VISION"

# JARVIS color palette
JARVIS_CYAN = (255, 220, 80)
JARVIS_BLUE = (255, 150, 40)


def main():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError(
            "Could not open the camera."
        )

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    detector = ObjectDetector()
    hud = XenoHUD()
    hand_tracker = HandTracker()
    effects = EnergyEffects()

    start_time = time.time()

    while True:

        success, frame = camera.read()

        if not success:
            print("Failed to read camera frame.")
            break

        frame = cv2.flip(
            frame,
            1
        )

        height, width = frame.shape[:2]

        hud.update(height)

        # =================================================
        # YOLO OBJECT DETECTION
        # =================================================

        results = detector.detect(frame)

        object_count = 0

        for result in results:

            for box in result.boxes:

                confidence = float(
                    box.conf[0]
                )

                # Ignore weak detections
                if confidence < 0.55:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                class_id = int(
                    box.cls[0]
                )

                class_name = result.names[
                    class_id
                ]

                object_count += 1

                hud.draw_target(
                    frame,
                    x1,
                    y1,
                    x2,
                    y2,
                    class_name,
                    confidence
                )

        # =================================================
        # HAND TRACKING
        # =================================================

        hand_results = hand_tracker.process(
            frame
        )

        pinch_points = []

        if hand_results.multi_hand_landmarks:

            for hand_landmarks in (
                hand_results.multi_hand_landmarks
            ):

                if hand_tracker.is_pinching(
                    hand_landmarks
                ):

                    point = (
                        hand_tracker
                        .get_pinch_point(
                            hand_landmarks
                        )
                    )

                    pinch_points.append(
                        point
                    )

        # =================================================
        # TWO-HAND JARVIS ENERGY LINK
        # =================================================

        if len(pinch_points) == 2:

            current_time = (
                time.time() - start_time
            )

            effects.draw_energy_thread(
                frame,
                pinch_points[0],
                pinch_points[1],
                current_time
            )

            cv2.putText(
                frame,
                "JARVIS LINK // ACTIVE",
                (30, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                JARVIS_CYAN,
                1,
                cv2.LINE_AA
            )

        # =================================================
        # HUD
        # =================================================

        hud.draw_scan_line(frame)

        hud.draw_interface(
            frame,
            object_count
        )

        # =================================================
        # DISPLAY
        # =================================================

        cv2.imshow(
            WINDOW_NAME,
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()