# Example usage for class SensorDataClient
from sensor_data_client import SensorDataClient

# Create a sensor data client instance
sensor_client = SensorDataClient()

# Get the latest RSSI data and its timestamp
timestamp_rssi, rssi_value = sensor_client.get_latest_rssi()
timestamp_temperature, temperature_value = sensor_client.get_latest_temperature()
timestamp_power, power_value = sensor_client.get_latest_pv_yield_power()


print(f"Latest RSSI value: {rssi_value} at {timestamp_rssi}")
print(f"Latest temperature value: {temperature_value} at {timestamp_temperature}")
print(f"Latest power value: {power_value} at {timestamp_temperature}")
print(timestamp_rssi)