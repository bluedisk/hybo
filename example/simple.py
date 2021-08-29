import time
import hybo

SERIAL_DEV = '/dev/cu.usbserial-D3095E6S'

with hybo.Lidar(SERIAL_DEV) as hybo:
    # waiting for first frame
    time.sleep(1)

    # retrieve latest frame
    frame = hybo.get_latest_frame()
    print(frame)