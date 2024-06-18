import DateTime

from sensor_data_client import SensorDataClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sensor_client = SensorDataClient()

wifi_data = {
        "timestamp": [],
        "rssi": [],
        "average": []
}
power_data = {
        "timestamp": [],
        "watt": [],
        "average": []
}
temperature_data = {
        "timestamp": [],
        "celsius": [],
        "average": []
}


# gets data and saves them in a accessible data-structure
def fetch_sensor_data(data_type):
        match data_type:
                case "wifi":
                        timestamp_rssi, rssi_value = sensor_client.get_latest_rssi()
                        wifi_data["timestamp"].append(DateTime.DateTime(timestamp_rssi))
                        wifi_data["rssi"].append(rssi_value)
                        wifi_data["average"].append(get_entry_average(wifi_data["rssi"]))
                case "power":
                        timestamp_watt, watt_value = sensor_client.get_latest_pv_yield_power()
                        power_data["timestamp"].append(DateTime.DateTime(timestamp_watt))
                        power_data["watt"].append(watt_value)
                        power_data["average"].append(get_entry_average(power_data["watt"]))
                case "temperature":
                        timestamp_celsius, celsius_value = sensor_client.get_latest_temperature()
                        temperature_data["timestamp"].append(DateTime.DateTime(timestamp_celsius))
                        temperature_data["celsius"].append(celsius_value)
                        temperature_data["average"].append(get_entry_average(temperature_data["celsius"]))


def get_entry_average(entries):
        value_sum = 0
        value_count = 0
        average = None
        for entry in entries:
                value_sum += entry  # sums up the value for each unit
                value_count += 1  # counts how many values have been added
                average = value_sum / value_count  # calculates average value so far
        return average


class Wifi():
        def __init__(self, timestamp, rssi):
                self.timestamp = timestamp
                self.rssi = rssi

        timestamp = 0
        rssi = 0
        average = 0


class Power():
        def __init__(self, timestamp, watt):
                self.timestamp = timestamp
                self.rssi = watt

        timestamp = 0
        watt = 0
        average = 0


class Temperature():
        def __init__(self, timestamp, celsius):
                self.timestamp = timestamp
                self.rssi = celsius

        timestamp = 0
        celsius = 0
        average = 0


from time import sleep

fetch_sensor_data("wifi")
fetch_sensor_data("power")
fetch_sensor_data("temperature")
sleep(120)
fetch_sensor_data("wifi")
fetch_sensor_data("power")
fetch_sensor_data("temperature")


def print_data_elements(data_dict, name):
        print(f"{name} Data:")
        for key, values in data_dict.items():
                print(f"{key.capitalize()}:")
                for i, value in enumerate(values):
                        print(f"  {i + 1}: {value}")
        print()


print_data_elements(wifi_data, "Wifi")
print_data_elements(power_data, "Power")
print_data_elements(temperature_data, "Temperature")
