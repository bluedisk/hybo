import time
import hybo

SERIAL_DEV = '/dev/cu.usbserial-D3095E6S'

hybo = hybo.Lidar(SERIAL_DEV)
hybo.start()

# waiting for first frame
time.sleep(1)

print(hybo.get_latest_frame())
hybo.close()
