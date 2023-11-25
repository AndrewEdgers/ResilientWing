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

SENSOR_DELAY = 1  # Sensor reading delay in seconds


def main():
    sensors.initialize()
    visualization.initialize()

    try:
        while True:
            accel_data, gyro_data = sensors.read_data()
            ax, ay, az = accel_data['x'], accel_data['y'], accel_data['z']
            visualization.update_visualization(ax, ay, az)
            visualization.draw()  # Ensure this is called each loop iteration

            if visualization.check_for_exit():
                break

            time.sleep(SENSOR_DELAY)
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        sensors.shutdown()
        visualization.shutdown()


if __name__ == "__main__":
    main()
