import cv2
import math
import time


class XenoHUD:

    # =====================================================
    # JARVIS COLOR PALETTE
    # =====================================================

    CYAN = (255, 220, 80)
    BRIGHT_CYAN = (255, 255, 180)
    BLUE = (255, 150, 40)
    DARK_BLUE = (180, 80, 20)
    WHITE = (255, 255, 255)
    STATUS = (255, 220, 120)

    def __init__(self):

        self.start_time = time.time()
        self.scan_position = 0
        self.rotation = 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, height: int):

        self.scan_position += 3

        if self.scan_position >= height:
            self.scan_position = 0

        self.rotation += 1

        if self.rotation >= 360:
            self.rotation = 0

    # =====================================================
    # TEXT
    # =====================================================

    @staticmethod
    def text(
        frame,
        value,
        position,
        size=0.5,
        thickness=1,
        color=(255, 220, 80)
    ):

        cv2.putText(
            frame,
            value,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            size,
            color,
            thickness,
            cv2.LINE_AA
        )

    # =====================================================
    # CORNER FRAME
    # =====================================================

    def draw_corner_frame(self, frame):

        h, w = frame.shape[:2]

        color = self.BLUE

        margin = 18
        length = 65

        # Top left
        cv2.line(
            frame,
            (margin, margin),
            (margin + length, margin),
            color,
            1
        )

        cv2.line(
            frame,
            (margin, margin),
            (margin, margin + length),
            color,
            1
        )

        # Top right
        cv2.line(
            frame,
            (w - margin, margin),
            (w - margin - length, margin),
            color,
            1
        )

        cv2.line(
            frame,
            (w - margin, margin),
            (w - margin, margin + length),
            color,
            1
        )

        # Bottom left
        cv2.line(
            frame,
            (margin, h - margin),
            (margin + length, h - margin),
            color,
            1
        )

        cv2.line(
            frame,
            (margin, h - margin),
            (margin, h - margin - length),
            color,
            1
        )

        # Bottom right
        cv2.line(
            frame,
            (w - margin, h - margin),
            (w - margin - length, h - margin),
            color,
            1
        )

        cv2.line(
            frame,
            (w - margin, h - margin),
            (w - margin, h - margin - length),
            color,
            1
        )

    # =====================================================
    # CENTER HUD
    # =====================================================

    def draw_center_hud(self, frame):

        h, w = frame.shape[:2]

        cx = w // 2
        cy = h // 2

        radius = 38

        # Outer circle
        cv2.circle(
            frame,
            (cx, cy),
            radius,
            self.BLUE,
            1
        )

        # Inner core
        cv2.circle(
            frame,
            (cx, cy),
            5,
            self.BRIGHT_CYAN,
            1
        )

        # Rotating arc
        cv2.ellipse(
            frame,
            (cx, cy),
            (radius + 12, radius + 12),
            self.rotation,
            20,
            120,
            self.CYAN,
            2
        )

        cv2.ellipse(
            frame,
            (cx, cy),
            (radius + 12, radius + 12),
            self.rotation + 180,
            20,
            120,
            self.BLUE,
            1
        )

        # Target lines
        cv2.line(
            frame,
            (cx - 75, cy),
            (cx - 45, cy),
            self.CYAN,
            1
        )

        cv2.line(
            frame,
            (cx + 45, cy),
            (cx + 75, cy),
            self.CYAN,
            1
        )

        cv2.line(
            frame,
            (cx, cy - 75),
            (cx, cy - 45),
            self.CYAN,
            1
        )

        cv2.line(
            frame,
            (cx, cy + 45),
            (cx, cy + 75),
            self.CYAN,
            1
        )

    # =====================================================
    # SCAN LINE
    # =====================================================

    def draw_scan_line(self, frame):

        h, w = frame.shape[:2]

        y = self.scan_position

        overlay = frame.copy()

        cv2.line(
            overlay,
            (30, y),
            (w - 30, y),
            self.CYAN,
            1
        )

        cv2.addWeighted(
            overlay,
            0.18,
            frame,
            0.82,
            0,
            frame
        )

    # =====================================================
    # GRID
    # =====================================================

    def draw_grid(self, frame):

        h, w = frame.shape[:2]

        overlay = frame.copy()

        spacing = 80

        for x in range(
            0,
            w,
            spacing
        ):

            cv2.line(
                overlay,
                (x, 0),
                (x, h),
                self.DARK_BLUE,
                1
            )

        for y in range(
            0,
            h,
            spacing
        ):

            cv2.line(
                overlay,
                (0, y),
                (w, y),
                self.DARK_BLUE,
                1
            )

        cv2.addWeighted(
            overlay,
            0.12,
            frame,
            0.88,
            0,
            frame
        )

    # =====================================================
    # OBJECT TARGET
    # =====================================================

    def draw_target(
        self,
        frame,
        x1,
        y1,
        x2,
        y2,
        label,
        confidence
    ):

        cyan = self.CYAN

        width = x2 - x1
        height = y2 - y1

        corner = max(
            18,
            min(width, height) // 5
        )

        # Top left
        cv2.line(
            frame,
            (x1, y1),
            (x1 + corner, y1),
            cyan,
            2
        )

        cv2.line(
            frame,
            (x1, y1),
            (x1, y1 + corner),
            cyan,
            2
        )

        # Top right
        cv2.line(
            frame,
            (x2, y1),
            (x2 - corner, y1),
            cyan,
            2
        )

        cv2.line(
            frame,
            (x2, y1),
            (x2, y1 + corner),
            cyan,
            2
        )

        # Bottom left
        cv2.line(
            frame,
            (x1, y2),
            (x1 + corner, y2),
            cyan,
            2
        )

        cv2.line(
            frame,
            (x1, y2),
            (x1, y2 - corner),
            cyan,
            2
        )

        # Bottom right
        cv2.line(
            frame,
            (x2, y2),
            (x2 - corner, y2),
            cyan,
            2
        )

        cv2.line(
            frame,
            (x2, y2),
            (x2, y2 - corner),
            cyan,
            2
        )

        # Center target

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.circle(
            frame,
            (cx, cy),
            4,
            self.BRIGHT_CYAN,
            -1
        )

        cv2.line(
            frame,
            (cx - 16, cy),
            (cx - 7, cy),
            cyan,
            1
        )

        cv2.line(
            frame,
            (cx + 7, cy),
            (cx + 16, cy),
            cyan,
            1
        )

        # Label

        text = (
            f"{label.upper()} // "
            f"{confidence * 100:.0f}%"
        )

        self.text(
            frame,
            text,
            (x1, max(y1 - 10, 20)),
            0.45,
            1,
            cyan
        )

    # =====================================================
    # TELEMETRY
    # =====================================================

    def draw_telemetry(
        self,
        frame,
        object_count
    ):

        h, w = frame.shape[:2]

        x = 30

        self.text(
            frame,
            "JARVIS CORE",
            (x, 105),
            0.48,
            1,
            self.CYAN
        )

        self.text(
            frame,
            "VISUAL MATRIX",
            (x, 128),
            0.40,
            1,
            self.STATUS
        )

        self.text(
            frame,
            "OBJECT TRACKING",
            (x, 151),
            0.40,
            1,
            self.STATUS
        )

        self.text(
            frame,
            f"ENTITIES  {object_count:02d}",
            (x, 174),
            0.40,
            1,
            self.BRIGHT_CYAN
        )

        rx = w - 190

        self.text(
            frame,
            "SYSTEM STATUS",
            (rx, 105),
            0.42,
            1,
            self.CYAN
        )

        self.text(
            frame,
            "CAMERA     ONLINE",
            (rx, 128),
            0.38,
            1,
            self.STATUS
        )

        self.text(
            frame,
            "YOLO       ACTIVE",
            (rx, 150),
            0.38,
            1,
            self.STATUS
        )

        self.text(
            frame,
            "HAND LINK  READY",
            (rx, 172),
            0.38,
            1,
            self.STATUS
        )

    # =====================================================
    # MAIN INTERFACE
    # =====================================================

    def draw_interface(
        self,
        frame,
        object_count
    ):

        h, w = frame.shape[:2]

        self.draw_grid(frame)

        self.draw_corner_frame(frame)

        self.draw_center_hud(frame)

        self.draw_telemetry(
            frame,
            object_count
        )

        # Main title

        self.text(
            frame,
            "XENO-VISION",
            (30, 40),
            0.82,
            2,
            self.BRIGHT_CYAN
        )

        self.text(
            frame,
            "COGNITIVE VISUAL INTERFACE",
            (32, 62),
            0.38,
            1,
            self.STATUS
        )

        # Online indicator

        cv2.circle(
            frame,
            (w - 175, 32),
            4,
            self.BRIGHT_CYAN,
            -1
        )

        self.text(
            frame,
            "SYSTEM ONLINE",
            (w - 160, 37),
            0.45,
            1,
            self.BRIGHT_CYAN
        )

        # Bottom status

        self.text(
            frame,
            "VISUAL MATRIX // ACTIVE",
            (30, h - 30),
            0.40,
            1,
            self.STATUS
        )

        self.text(
            frame,
            "JARVIS LINK // READY",
            (w - 180, h - 30),
            0.40,
            1,
            self.STATUS
        )