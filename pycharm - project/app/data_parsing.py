''''# Example usage for class SensorDataClient
from sensor_data_client import SensorDataClient

# Create a sensor data client instance
sensor_client = SensorDataClient()

# Get the latest RSSI data and its timestamp
timestamp, rssi_value = sensor_client.get_latest_rssi()
if timestamp and rssi_value is not None:
    print(f"Latest RSSI value: {rssi_value} at {timestamp}")
else:
    print("No data found.")
'''


import datetime

print(datetime.datetime.now())