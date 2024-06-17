from flask import Flask, request, render_template
from flask_mongoengine2 import MongoEngine
from mongoengine import Document
from mongoengine.fields import DateTimeField, IntField, FloatField
from random import randint
from datetime import datetime



#region helper functions
# create_entries_dictionary: calculates average and generalizes the rssi/watt/celsius into "unit"
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
    wifi = Wifi(timestamp=datetime.now(), rssi=randint(-100,-50))
    wifi.save()
def add_power():
    power = Power(timestamp=datetime.now(), watt=randint(0,99))
    power.save()
def add_temperature():
    temperature = Temperature(timestamp=datetime.now(), celsius=randint(-10,40))
    temperature.save()
#endregion





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


app.run(host='0.0.0.0', port=5000)