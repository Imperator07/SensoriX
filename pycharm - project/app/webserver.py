
from flask import Flask, request, render_template
import io

from flask import Flask
from flask import Flask, request, render_template, send_file
from flask_mongoengine2 import MongoEngine
from mongoengine import Document
from mongoengine.fields import DateTimeField, IntField, FloatField
from random import randint
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy.sql.functions import random


from sensor_data_client import SensorDataClient

#region helper functions
# create_entries_dictionary: calculates average and generalizes the rssi/watt/celsius into "unit"
data = {
    "timestamps": [],
    "values": []
}

def fetch_sensor_data():
    now = datetime.now()
    value = 1
    data["timestamps"].append(now)
    data["values"].append(value)
    if len(data["timestamps"]) > 10:#Keep only the latest 10 data points
        data["timestamps"].pop(0)
        data["values"].pop(0)
def create_entries_dictionary(entries, unit_field, short_unit_field):
    formatted_entries = []
    value_sum = 0
    value_count = 0
    for entry in entries:
        value_sum += getattr(entry, unit_field) #generalized version of entry.rssi/watt/celsius
        value_count += 1
        average = value_sum / value_count
        formatted_entries.append({
            'timestamp': entry.timestamp,
            'unit': str(getattr(entry, unit_field)) + short_unit_field, #formatted with the unit symbol
            'average': str(round(average, 2)) + short_unit_field
        })
    return formatted_entries

def add_wifi():
    timestamp_rssi, rssi_value = sensor_client.get_latest_rssi()
    wifi = Wifi(timestamp=timestamp_rssi, rssi=rssi_value)
    wifi.save()
def add_power():
    timestamp_power, power_value = sensor_client.get_latest_pv_yield_power()






    power = Power(timestamp=timestamp_power, watt=power_value)
    power.save()
def add_temperature():
    timestamp_temperature, temperature_value = sensor_client.get_latest_temperature()
    temperature = Temperature(timestamp=timestamp_temperature, celsius=temperature_value)
    temperature.save()
#endregion



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
    add_wifi()
    entries = Wifi.objects.all()
    formatted_entries = create_entries_dictionary(entries, "rssi", " dBm")
    return render_template('output.html', measurement="Wifi-Traffic", unit='RSSI', entries=formatted_entries)


@app.route("/power")
def power():
    add_power()
    entries = Power.objects.all()
    entries = Power.objects.all()
    formatted_entries = create_entries_dictionary(entries, "watt", " W")
    return render_template('output.html', measurement="Power Generation", unit='Watt', entries=formatted_entries)


@app.route("/temperature")
def temperature():
    add_temperature()
    entries = Temperature.objects.all()
    entries = Temperature.objects.all()
    formatted_entries = create_entries_dictionary(entries, "celsius", "° C")
    return render_template('output.html', measurement="Temperature", unit='Celsius', entries=formatted_entries)

@app.route('/plot.png')
def plot_png():
    fetch_sensor_data()  # Update data from sensors

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data["timestamps"], data["values"])

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