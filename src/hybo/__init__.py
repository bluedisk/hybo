import struct
from functools import partial

import numpy as np
import serial
from serial.threaded import Packetizer, ReaderThread

HYBO_PACKET_SIZE = 2904


class LidarPacketizer(Packetizer):
    TERMINATOR = b'\x5A\xA5\x5A\xA5'

    def __init__(self, on_frame=None):
        super().__init__()
        self.on_frame = on_frame

    def handle_packet(self, packet):
        #  0: packet size(4),
        #  4: frame sequence(2),
        #  6: data type(2, not using, fixed),
        #  8: time_peak_sec(4), time_peak_ms(4),
        # 16: time_imu_sec(4, not working), time_imu_ms(4, not working)
        # 24: point data(2880) = [x(2), y(2), x(2)] * 480
        # -4: checksum(4)

        packet_size, seq = struct.unpack("<IH", packet[:6])
        checksum, = struct.unpack("<I", packet[-4:])

        is_valid = packet_size == HYBO_PACKET_SIZE and checksum == sum(packet[4:-4])
        if not is_valid:
            return

        time_peak = ".".join(struct.unpack("<II", packet[8:16]))

        # parse points
        points = np.frombuffer(packet[24:-4], dtype='int16').reshape(-1, 3)

        if self.on_frame:
            self.on_frame({
                "sequence": seq,
                "time_peak": float(time_peak),
                "points": points
            })


class Lidar:
    def __init__(self, port, baudrate=921600, timeout=50):
        self.serial = serial.serial_for_url(port, baudrate=baudrate, timeout=timeout)
        self.reader = None
        self.callback = None
        self.latest_frame = None

    def start(self, callback=None):
        self.reader = ReaderThread(self.serial, partial(LidarPacketizer, self._on_frame))
        self.callback = callback

        self.reader.start()
        self.reader.connect()

        return self

    def close(self):
        self.reader.close()

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _on_frame(self, frame):
        self.latest_frame = frame

    def get_latest_frame(self):
        return self.latest_frame
