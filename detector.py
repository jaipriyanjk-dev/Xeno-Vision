from ultralytics import YOLO


class ObjectDetector:

    def __init__(
        self,
        model_name: str = "yolo11s.pt"
    ) -> None:

        self.model = YOLO(model_name)

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            imgsz=960,
            conf=0.55,
            iou=0.45,
            verbose=False
        )

        return results