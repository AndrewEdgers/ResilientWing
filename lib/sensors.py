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

import smbus2 as smbus
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
        try:
            self.bus = smbus.SMBus(bus_num)
            self.address = address
            self.bus.write_byte_data(self.address, self.POWER_MGMT_1, 0)
            self.last_time = time.time()
            self.angle_x = self.angle_y = self.angle_z = 0.0

            # Initialize gyro offset values
            self.gyro_offset_x = 0.0
            self.gyro_offset_y = 0.0
            self.gyro_offset_z = 0.0

        except Exception as e:
            print(f"Error initializing MPU6050: {e}")
            raise

    def calibrate_gyro(self, samples=100):
        print("Calibrating gyroscope. Keep the sensor stationary...")
        offset_x, offset_y, offset_z = 0, 0, 0
        for _ in range(samples):
            data = self.get_gyro_data()
            offset_x += data['x']
            offset_y += data['y']
            offset_z += data['z']
            time.sleep(0.01)  # Short delay between readings

        self.gyro_offset_x = offset_x / samples
        self.gyro_offset_y = offset_y / samples
        self.gyro_offset_z = offset_z / samples
        print("Calibration complete")

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
        try:
            radians_x = math.atan2(y, self._dist(x, z))
            radians_y = math.atan2(x, self._dist(y, z))
            return {
                'x': math.degrees(radians_x),
                'y': -math.degrees(radians_y)
            }
        except Exception as e:
            print(f"Error calculating rotation: {e}")
            raise

    @staticmethod
    def _dist(a, b):
        return math.sqrt(a * a + b * b)

    GYRO_NOISE_THRESHOLD = 1  # Gyroscope noise threshold

    def get_gyro_data(self):
        try:
            x = self._read_word_2c(self.GYRO_XOUT) / 131
            y = self._read_word_2c(self.GYRO_YOUT) / 131
            z = self._read_word_2c(self.GYRO_ZOUT) / 131

            x -= self.gyro_offset_x
            y -= self.gyro_offset_y
            z -= self.gyro_offset_z

            # Apply noise threshold
            x = x if abs(x) > self.GYRO_NOISE_THRESHOLD else 0
            y = y if abs(y) > self.GYRO_NOISE_THRESHOLD else 0
            z = z if abs(z) > self.GYRO_NOISE_THRESHOLD else 0

            return {'x': x, 'y': y, 'z': z}
        except Exception as e:
            print(f"Error reading gyroscope data: {e}")
            raise

    def get_accel_data(self):
        try:
            x = self._read_word_2c(self.ACCEL_XOUT) / 16384.0
            y = self._read_word_2c(self.ACCEL_YOUT) / 16384.0
            z = self._read_word_2c(self.ACCEL_ZOUT) / 16384.0
            return {'x': x, 'y': y, 'z': z}
        except Exception as e:
            print(f"Error reading accelerometer data: {e}")
            raise

    def get_rotation_angles(self):
        accel_data = self.get_accel_data()
        return self._get_rotation(accel_data['x'], accel_data['y'], accel_data['z'])

    def integrate_gyro(self, gyro_data):
        current_time = time.time()
        delta_t = current_time - self.last_time
        self.last_time = current_time

        # Integrate gyro data (convert to degrees and accumulate)
        self.angle_x += gyro_data['x'] * delta_t
        self.angle_y += gyro_data['y'] * delta_t
        self.angle_z += gyro_data['z'] * delta_t

        return {'x': self.angle_x, 'y': self.angle_y, 'z': self.angle_z}

    def read_data(self):
        accel_data = self.get_accel_data()
        gyro_data = self.get_gyro_data()

        # Integrate gyro data to get angles
        gyro_angles = self.integrate_gyro(gyro_data)

        # Use a complementary filter to combine gyro and accel data
        accel_angles = self.get_rotation_angles()
        alpha = 0.98  # Complementary filter constant

        filtered_angle_x = alpha * gyro_angles['x'] + (1 - alpha) * accel_angles['x']
        filtered_angle_y = alpha * gyro_angles['y'] + (1 - alpha) * accel_angles['y']
        # For Z-axis, you might rely solely on gyro as accel doesn't provide yaw info

        return {'x': filtered_angle_x, 'y': filtered_angle_y, 'z': gyro_angles['z']}


_sensor_instance = None


def initialize():
    """
    Initializes the sensor for use.
    """
    global _sensor_instance
    _sensor_instance = MPU6050()
    _sensor_instance.calibrate_gyro()


def read_data():
    """
    Reads data from the sensor.
    :return: tuple containing accelerometer and gyroscope data.
    """
    global _sensor_instance
    if _sensor_instance is None:
        raise Exception("Sensor is not initialized. Call initialize() first.")
    return _sensor_instance.read_data()


def shutdown():
    """
    Shutdown the sensor. Currently, the MPU6050 doesn't have a specific shutdown method,
    so this function is left as a placeholder for any cleanup you might want to add in the future.
    """
    pass  # No specific shutdown procedure for MPU6050 in this setup, but kept for future additions or modifications.


def main():
    sensor = MPU6050()
    sensor.calibrate_gyro()
    try:
        while True:
            gyro_data = sensor.get_gyro_data()
            accel_data = sensor.get_accel_data()
            rotation = sensor.get_rotation_angles()

            print("Gyroscope Data (°/s): X: {:.3f}, Y: {:.3f}, Z: {:.3f}".format(gyro_data['x'], gyro_data['y'],
                                                                                 gyro_data['z']))
            print("Accelerometer Data (g): X: {:.3f}, Y: {:.3f}, Z: {:.3f}".format(accel_data['x'], accel_data['y'],
                                                                                   accel_data['z']))
            print("Rotation Angles (°): X: {:.3f}, Y: {:.3f}, Z: {:.3f}".format(rotation['x'], rotation['y'],
                                                                                rotation['z']))
            print("-------------------------------------------------------")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Sensor test terminated by user.")


if __name__ == "__main__":
    main()
