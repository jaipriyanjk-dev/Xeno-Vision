import cv2
import math
import random


class EnergyEffects:
    CYAN = (255, 220, 80)
    BRIGHT_CYAN = (255, 255, 180)
    BLUE = (255, 150, 40)

    @staticmethod
    def draw_energy_thread(frame, point1, point2, time_value):
        h, w = frame.shape[:2]

        x1 = int(point1[0] * w)
        y1 = int(point1[1] * h)

        x2 = int(point2[0] * w)
        y2 = int(point2[1] * h)

        dx = x2 - x1
        dy = y2 - y1

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 20:
            return

        # Main energy connection
        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            EnergyEffects.CYAN,
            3
        )

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            EnergyEffects.BRIGHT_CYAN,
            1
        )

        # Secondary energy threads
        offset = 4
        length = max(distance, 1)

        nx = -dy / length
        ny = dx / length

        p1a = (
            int(x1 + nx * offset),
            int(y1 + ny * offset)
        )

        p2a = (
            int(x2 + nx * offset),
            int(y2 + ny * offset)
        )

        p1b = (
            int(x1 - nx * offset),
            int(y1 - ny * offset)
        )

        p2b = (
            int(x2 - nx * offset),
            int(y2 - ny * offset)
        )

        cv2.line(
            frame,
            p1a,
            p2a,
            EnergyEffects.BLUE,
            1
        )

        cv2.line(
            frame,
            p1b,
            p2b,
            EnergyEffects.BLUE,
            1
        )

        # Moving energy particles
        particle_count = max(
            8,
            int(distance / 18)
        )

        for i in range(particle_count):

            progress = (
                i / particle_count
                + time_value * 0.6
            ) % 1.0

            px = int(x1 + dx * progress)
            py = int(y1 + dy * progress)

            radius = random.choice([
                1, 1, 2, 2, 3
            ])

            cv2.circle(
                frame,
                (px, py),
                radius,
                EnergyEffects.BRIGHT_CYAN,
                -1
            )

        # Energy nodes
        for px, py in [(x1, y1), (x2, y2)]:

            cv2.circle(
                frame,
                (px, py),
                15,
                EnergyEffects.BLUE,
                1
            )

            cv2.circle(
                frame,
                (px, py),
                7,
                EnergyEffects.CYAN,
                2
            )

            cv2.circle(
                frame,
                (px, py),
                3,
                EnergyEffects.BRIGHT_CYAN,
                -1
            )

        # Small energy sparks
        for px, py in [(x1, y1), (x2, y2)]:

            for _ in range(7):

                angle = random.uniform(
                    0,
                    math.pi * 2
                )

                spark_length = random.randint(
                    7,
                    25
                )

                sx = int(
                    px + math.cos(angle) * spark_length
                )

                sy = int(
                    py + math.sin(angle) * spark_length
                )

                cv2.line(
                    frame,
                    (px, py),
                    (sx, sy),
                    EnergyEffects.CYAN,
                    1
                )