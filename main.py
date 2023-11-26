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

import time
from lib import sensors, visualization

# Initial orientation (in degrees)
ax, ay, az = 0.0, 0.0, 0.0
gx, gy, gz = 0.0, 0.0, 0.0

# Initial time
last_time = time.time()

SENSOR_DELAY = 0.1  # Sensor reading delay in seconds


def main():
    global ax, ay, az, gx, gy, gz, last_time

    sensors.initialize()
    visualization.initialize()

    try:
        while True:
            # current_time = time.time()
            # delta_t = current_time - last_time  # Calculate elapsed time

            # accel_data, gyro_data = sensors.read_data()
            rotation_data = sensors.read_data()

            # Integrate the gyroscope data
            # gx += gyro_data['x'] * delta_t
            # gy += gyro_data['y'] * delta_t
            # gz += gyro_data['z'] * delta_t

            # ax, ay, az = accel_data['x'], accel_data['y'], accel_data['z']
            # gx, gy, gz = gyro_data['x'], gyro_data['y'], gyro_data['z']
            # print(f"Updating visualization with: ax={ax}, ay={ay}, az={az}")
            # print(f"Updating visualization with: gx={gx}, gy={gy}, gz={gz}")

            # visualization.update_visualization(ax, ay, az)
            # visualization.update_visualization(gx, gy, gz)
            visualization.update_visualization(rotation_data['x'], rotation_data['y'], rotation_data['z'])
            visualization.draw()  # Ensure this is called each loop iteration

            if visualization.check_for_exit():
                break

            # Update the last time
            # last_time = current_time

            time.sleep(SENSOR_DELAY)

    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        sensors.shutdown()
        visualization.shutdown()


if __name__ == "__main__":
    main()
