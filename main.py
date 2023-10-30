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
from lib import sensors


def main():
    # Initialize the sensor module
    sensors.initialize()

    try:
        while True:
            # Get accelerometer and gyroscope data
            accel_data, gyro_data = sensors.read_data()

            # Print the data (or you can process or send it wherever needed)
            print("Accelerometer Data:", accel_data)
            print("Gyroscope Data:", gyro_data)

            # You can add more logic here, like checking if the UAV is
            # operating within safe parameters, and reacting accordingly

            time.sleep(1)  # Adjust the delay as needed

    except KeyboardInterrupt:
        print("Program stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up and shut down
        sensors.shutdown()


if __name__ == "__main__":
    main()

