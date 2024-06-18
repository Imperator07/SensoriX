# TODO: find a way to parse the data type to the plot function

import io

from flask import Flask, request, render_template, send_file
from flask_mongoengine2 import MongoEngine
from mongoengine import Document
from mongoengine.fields import DateTimeField, IntField, FloatField
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import DateTime
from sensor_data_client import SensorDataClient


sensor_client = SensorDataClient()


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "sensorix_db",
    "host": "10.115.2.53",
    "port": 27017,
    "username": "admin",
    "password": "abcd1234!"
}


db = MongoEngine(app)





# gets data and saves them in a accessible data-structure
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
                        wifi_data["timestamp"].append(timestamp_rssi)
                        wifi_data["rssi"].append(rssi_value)
                        wifi_data["average"].append(get_entry_average(wifi_data["rssi"]))

                        if len(wifi_data["timestamp"]) > 1 and wifi_data["timestamp"][-1] != wifi_data["timestamp"][-2]:
                                # if there are two entries AND those are different we update the database
                                # otherwise we would flood the db with the same entries
                                # we do however need wifi_data to contain all data for the plot (which updates periodically)
                                wifi = Wifi(timestamp=wifi_data["timestamp"][-1],
                                            rssi=wifi_data["rssi"][-1],
                                            average=wifi_data["average"][-1])
                                wifi.save()


                        # we dont want to show the entire history on the graph so we remove the entries older than 15
                        if len(wifi_data["timestamp"]) >= 15:
                                length = len(wifi_data["timestamp"])
                                print(f"removed last index because length was: {length}")
                                wifi_data["timestamp"].pop(0)
                                wifi_data["rssi"].pop(0)
                                wifi_data["average"].pop(0)

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

                case "all":
                        fetch_sensor_data("wifi")
                        fetch_sensor_data("power")
                        fetch_sensor_data("temperature")

def get_entry_average(entries):
        value_sum = 0
        value_count = 0
        average = None
        for entry in entries:
                value_sum += entry  # sums up the value for each unit
                value_count += 1  # counts how many values have been added
                average = value_sum / value_count  # calculates average value so far
        return average


def format_entries(entries, unit):
        formated_entries = []

        for entry in entries:
                formated_entry = {
                        "timestamp": entry.timestamp,
                        "unit": getattr(entry, unit),
                        "average": entry.average,
                }
                formated_entries.append(formated_entry)

        return formated_entries

#endregion






class Wifi(Document):
    timestamp = DateTimeField()
    rssi = IntField()
    average = FloatField(required=False)
class Power(Document):
    timestamp = DateTimeField()
    watt = IntField()
    average = FloatField(required=False)
class Temperature(Document):
    timestamp = DateTimeField()
    celsius = IntField()
    average = FloatField(required=False)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wifi")
def wifi():
    entries = Wifi.objects.all()
    formated_entries = format_entries(entries, "rssi")
    return render_template('output_with_plot.html', measurement="Wifi-Traffic", measure='RSSI', unit="dBm", entries=formated_entries)


@app.route("/power")
def power():
    entries = Power.objects.all()
    return render_template('output_with_plot.html', measurement="Power Generation", measure='Watt', unit="W", entries=entries)


@app.route("/temperature")
def temperature():
    entries = Temperature.objects.all()
    return render_template('output_with_plot.html', measurement="Temperature", measure='Celsius', unit="°C", entries=entries)



@app.route('/plot.png')
def plot_png(data_type):
    fetch_sensor_data(data_type)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    match data_type:
            case "wifi":
                    ax.plot(wifi_data["timestamp"], wifi_data["rssi"])
            case "power":
                    ax.plot(power_data["timestamp"], power_data["watt"])
            case "temperature":
                    ax.plot(temperature_data["timestamp"], temperature_data["celsius"])

    # Format the x-axis to show timestamps properly
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()  # Rotate date labels

    ax.set_title('Real-Time Sensor Data')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Value')
    ax.grid(True)

    # Save it to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')



app.run(host='0.0.0.0', port=5000)