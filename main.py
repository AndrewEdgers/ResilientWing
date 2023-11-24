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


def main():
    # Initialize the sensor module
    sensors.initialize()
    visualization.initialize()

    try:
        while True:
            # Get accelerometer and gyroscope data
            # accel_data, gyro_data = sensors.read_data()
            ax, ay, az = sensors.read_data()

            # Print the data
            print("Accelerometer and Gyroscope Data:", ax, ay, az)

            visualization.update_visualization(ax, ay, az)
            visualization.check_for_exit()

            time.sleep(1)  # Adjust the delay as needed

    except KeyboardInterrupt:
        print("Program stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up and shut down
        sensors.shutdown()
        visualization.shutdown()


if __name__ == "__main__":
    main()
