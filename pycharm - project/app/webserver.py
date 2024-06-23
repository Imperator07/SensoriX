import io
from flask import Flask, render_template, make_response
from flask_mongoengine2 import MongoEngine
from mongoengine import Document
from mongoengine.fields import DateTimeField, IntField, FloatField
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sensor_data_client import SensorDataClient


MAX_PLOT_POINT_AMOUNT = 15
DECIMAL_PRECISION = 2



sensor_client = SensorDataClient()


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "sensorix_db",
    "host": "",#"10.115.2.53",
    "port": 27017,
    "username": "admin",
    "password": "abcd1234!"
}


db = MongoEngine(app)





# gets data and saves them in a accessible data-structure
wifi_data = {
        "timestamp_now": [],
        "timestamp_sensor": [],
        "rssi": [],
        "average": []
}
power_data = {
        "timestamp_now": [],
        "timestamp_sensor": [],
        "watt": [],
        "average": []
}
temperature_data = {
        "timestamp_now": [],
        "timestamp_sensor": [],
        "celsius": [],
        "average": []
}


def output_data(data, title):
        print(f"{title}:")
        for key, values in data.items():
            print((f"\t{key}: {values}"))


# gets data and saves them in a accessible data-structure
def fetch_sensor_data(data_type):
    match data_type:
        case "wifi":
            timestamp_rssi, rssi_value = sensor_client.get_latest_rssi()
            wifi_data["timestamp_now"].append(datetime.now())
            wifi_data["timestamp_sensor"].append(timestamp_rssi)
            wifi_data["rssi"].append(rssi_value)
            wifi_data["average"].append(round(get_entry_average(wifi_data["rssi"]), DECIMAL_PRECISION))

            #output_data(wifi_data, "fetching wifi:")



            if len(wifi_data["timestamp_sensor"]) > 1 and wifi_data["timestamp_sensor"][-1] != wifi_data["timestamp_sensor"][-2]:
                wifi = Wifi(timestamp=wifi_data["timestamp_sensor"][-1],
                            rssi=wifi_data["rssi"][-1],
                            average=wifi_data["average"][-1])
                wifi.save()

        case "power":
            timestamp_watt, watt_value = sensor_client.get_latest_pv_yield_power()
            power_data["timestamp_now"].append(datetime.now())
            power_data["timestamp_sensor"].append(timestamp_watt)
            power_data["watt"].append(watt_value)
            power_data["average"].append(round(get_entry_average(power_data["watt"]), DECIMAL_PRECISION))

            #output_data(wifi_data, "fetching power:")


            if len(power_data["timestamp_sensor"]) > 1 and power_data["timestamp_sensor"][-1] != power_data["timestamp_sensor"][-2]:
                power = Power(timestamp=power_data["timestamp_sensor"][-1],
                              watt=power_data["watt"][-1],
                              average=power_data["average"][-1])
                power.save()

        case "temperature":
            timestamp_celsius, celsius_value = sensor_client.get_latest_temperature()
            temperature_data["timestamp_now"].append(datetime.now())
            temperature_data["timestamp_sensor"].append(timestamp_celsius)
            temperature_data["celsius"].append(celsius_value)
            temperature_data["average"].append(round(get_entry_average(temperature_data["celsius"]), DECIMAL_PRECISION))

            #output_data(wifi_data, "fetching temperature:")



            if len(temperature_data["timestamp_sensor"]) > 1 and temperature_data["timestamp_sensor"][-1] != temperature_data["timestamp_sensor"][-2]:
                temperature = Temperature(timestamp=temperature_data["timestamp_sensor"][-1],
                                          celsius=temperature_data["celsius"][-1],
                                          average=temperature_data["average"][-1])
                temperature.save()


    for data_type in [wifi_data, power_data, temperature_data]:
            if len(data_type["timestamp_now"]) >= MAX_PLOT_POINT_AMOUNT:
                    for key, value in data_type.items():
                        value.pop(0)



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
                        "timestamp": entry.timestamp.strftime('%H:%M:%S'),
                        "unit": getattr(entry, unit),
                        "average": entry.average,
                }
                formated_entries.append(formated_entry)

        formated_entries = reversed(formated_entries)

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
        if len(wifi_data["timestamp_sensor"]) > 1:
                wifi = Wifi(timestamp=wifi_data["timestamp_sensor"][-1],
                            rssi=wifi_data["rssi"][-1],
                            average=wifi_data["average"][-1])
                wifi.save()


        entries = Wifi.objects.all()
        formated_entries = format_entries(entries, "rssi")

        unit_data = {
            "heading": "Wifi-Traffic",
            "table_head": "RSSI",
            "unit": "dBm"
        }

        return render_template('output.html', unit_data=unit_data, entries=formated_entries)


@app.route("/power")
def power():
        if len(power_data["timestamp_sensor"]) > 1:
                power = Power(timestamp=power_data["timestamp_sensor"][-1],
                              watt=power_data["watt"][-1],
                              average=power_data["average"][-1])
                power.save()




        entries = Power.objects.all()
        formated_entries = format_entries(entries, "watt")

        unit_data = {
                "heading": "Power Generation",
                "table_head": "Watt",
                "unit": "W"
        }
        return render_template('output.html', unit_data=unit_data, entries=formated_entries)


@app.route("/temperature")
def temperature():
        if (len(temperature_data["timestamp_sensor"]) >= 1):
                temperature = Temperature(timestamp=temperature_data["timestamp_sensor"][-1],
                                          celsius=temperature_data["celsius"][-1],
                                          average=temperature_data["average"][-1])
                temperature.save()


        entries = Temperature.objects.all()
        formated_entries = format_entries(entries, "celsius")

        unit_data = {
            "heading": "Temperature",
            "table_head": "Celsius",
            "unit": "°C"
        }
        return render_template('output.html', unit_data=unit_data, entries=formated_entries)


@app.route('/plot/<data_type>')
def plot_png(data_type):
    print(data_type)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    today = datetime.today().strftime('%Y-%m-%d')
    fetch_sensor_data(data_type)
    if data_type == 'wifi':
        if wifi_data["timestamp_now"] and wifi_data["rssi"]:
            ax.plot(wifi_data["timestamp_now"], wifi_data["rssi"], marker='.', linestyle='-', lw=2)
            ax.set_title(f'Wifi Strength ({today})')
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('RSSI')

    elif data_type == 'power':
        if power_data["timestamp_now"] and power_data["watt"]:
            ax.plot(power_data["timestamp_now"], power_data["watt"], marker='.', linestyle='-', lw=2)
            ax.set_title(f'Power Generation ({today})')
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Power (Watts)')

    elif data_type == 'temperature':
        if temperature_data["timestamp_now"] and temperature_data["celsius"]:
            ax.plot(temperature_data["timestamp_now"], temperature_data["celsius"], marker='.', linestyle='-', lw=2)
            ax.set_title(f'Temperature ({today})')
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Temperature (°C)')

    else:
        ax.plot([1, 2, 3, 4], [0, 0, 0, 0])
        ax.set_title('Not found')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()  # Rotate date labels


    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)

    plt.close(fig)
    return make_response(output.getvalue(), {'Content-Type': 'image/png'})






app.run(host='0.0.0.0', port=5000)