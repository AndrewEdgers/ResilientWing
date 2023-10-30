"""
Copyright Edgers 2023

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import smbus
import math
import time


class MPU6050:
    # MPU-6050 Registers
    POWER_MGMT_1 = 0x6b
    GYRO_XOUT = 0x43
    GYRO_YOUT = 0x45
    GYRO_ZOUT = 0x47
    ACCEL_XOUT = 0x3b
    ACCEL_YOUT = 0x3d
    ACCEL_ZOUT = 0x3f

    def __init__(self, address=0x68, bus_num=1):
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        # Wake up sensor
        self.bus.write_byte_data(self.address, self.POWER_MGMT_1, 0)

    def _read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr + 1)
        val = (high << 8) + low
        return val

    def _read_word_2c(self, adr):
        val = self._read_word(adr)
        if val >= 0x8000:
            return -(65536 - val)
        return val

    def _get_rotation(self, x, y, z):
        radians_x = math.atan2(y, self._dist(x, z))
        radians_y = math.atan2(x, self._dist(y, z))
        return {
            'x': math.degrees(radians_x),
            'y': -math.degrees(radians_y)
        }

    @staticmethod
    def _dist(a, b):
        return math.sqrt(a * a + b * b)

    def get_gyro_data(self):
        x = self._read_word_2c(self.GYRO_XOUT) / 131
        y = self._read_word_2c(self.GYRO_YOUT) / 131
        z = self._read_word_2c(self.GYRO_ZOUT) / 131
        return {'x': x, 'y': y, 'z': z}

    def get_accel_data(self):
        x = self._read_word_2c(self.ACCEL_XOUT) / 16384.0
        y = self._read_word_2c(self.ACCEL_YOUT) / 16384.0
        z = self._read_word_2c(self.ACCEL_ZOUT) / 16384.0
        return {'x': x, 'y': y, 'z': z}

    def get_rotation_angles(self):
        accel_data = self.get_accel_data()
        return self._get_rotation(accel_data['x'], accel_data['y'], accel_data['z'])


if __name__ == "__main__":
    sensor = MPU6050()

    while True:
        gyro_data = sensor.get_gyro_data()
        accel_data = sensor.get_accel_data()
        rotation = sensor.get_rotation_angles()

        print("Gyroscope Data (°/s): X: {:.3f}, Y: {:.3f}, Z: {:.3f}".format(gyro_data['x'], gyro_data['y'],
                                                                             gyro_data['z']))
        print("Accelerometer Data (g): X: {:.3f}, Y: {:.3f}, Z: {:.3f}".format(accel_data['x'], accel_data['y'],
                                                                               accel_data['z']))
        print("Rotation Angles (°): X: {:.3f}, Y: {:.3f}".format(rotation['x'], rotation['y']))
        print("-------------------------------------------------------")

        time.sleep(1)
