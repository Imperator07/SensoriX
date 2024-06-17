from sensor_data_client import SensorDataClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sensor_client = SensorDataClient()

data = {
    "timestamps": {
        "time_wifi": [],
        "time_power": [],
        "time_temp": []
    },
    "values": {
        "value_wifi": [],
        "value_power": [],
        "value_temp": []
    },
    "averages": {
        "avg_wifi": [],
        "avg_power": [],
        "avg_temp": []
    }
}



# gets data and saves them in a accessible data-structure
def fetch_sensor_data():                                                                                                # TODO: replace the 1 values with the actual fetching with the api
    # get data
    timestamp_rssi, rssi_value, timestamp_power, power_value, timestamp_temperature, temperature_value = 1,1, 1,1, 1,1

    '''timestamp_rssi, rssi_value = sensor_client.get_latest_rssi()
    timestamp_power, power_value = sensor_client.get_latest_pv_yield_power()
    timestamp_temperature, temperature_value = sensor_client.get_latest_temperature()'''
    # append timestamps
    data["timestamps"]["time_wifi"].append(timestamp_rssi)
    data["timestamps"]["time_power"].append(timestamp_power)
    data["timestamps"]["time_temp"].append(timestamp_temperature)
    # append values
    data["values"]["value_wifi"].append(rssi_value)
    data["values"]["value_power"].append(power_value)
    data["values"]["value_temp"].append(temperature_value)
    # calculate averages

    data["averages"]["avg_wifi"].append(get_entry_average(data["values"]["value_wifi"]))
    data["averages"]["avg_power"].append(get_entry_average(data["values"]["value_power"]))
    data["averages"]["avg_temp"].append(get_entry_average(data["values"]["value_temp"]))



def get_entry_average(entries):
    entry_averages = []
    value_sum = 0
    value_count = 0
    for entry in entries:
        value_sum += entry # sums up the value for each unit
        value_count += 1                        # counts how many values have been added
        average = value_sum / value_count       # calculates average value so far
        entry_averages.append(round(average, 2))
    return entry_averages






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




fetch_sensor_data()
print(data)