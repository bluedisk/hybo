import cv2
import hybo
import numpy as np

SCALE = 0.5
WIDTH = 2000
HEIGHT = 2000

HCENTER = int(WIDTH / 2)

DOT_COLOR = (200, 200, 255)
DOT_SIZE = 3

LIDAR_COLOR = (200, 255, 200)
LIDAR_SIZE = 10

SERIAL_DEV = '/dev/cu.usbserial-D3095E6S'

if __name__ == "__main__":
    with hybo.Lidar(SERIAL_DEV) as hybo:
        print("Start!")

        while cv2.waitKey(1) != 13:
            # retrieve one frame
            frame = hybo.get_latest_frame()
            if not frame:
                continue

            # make a background canvas
            img = np.zeros((WIDTH, HEIGHT, 3), np.uint8)
            cv2.circle(img, (HCENTER, 0), LIDAR_SIZE, LIDAR_COLOR)

            # points projection
            points = frame['points'] * SCALE
            points += (HCENTER, HEIGHT, 0)
            points = points.clip(min=0, max=min(WIDTH, HEIGHT))

            # draw points
            for x, y, _ in points:
                cv2.circle(img, (x, y), DOT_SIZE, DOT_COLOR)

            # update image
            cv2.flip(img, 0)
            cv2.imshow("Lidar", img)
