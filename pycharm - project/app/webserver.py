from flask import Flask
from flask import Flask, request, render_template
from flask_mongoengine2 import MongoEngine
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import DateTimeField, IntField, FloatField
from json import JSONEncoder
import datetime

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "sensorix_db",
    "host": "",
    "port": 27017,
    "username": "admin",
    "password": "abcd1234!"
}


db = MongoEngine(app)


class Wifi(Document):
    timestamp = DateTimeField()
    RSSI = IntField()
    average = FloatField()
class Power(Document):
    timestamp = DateTimeField()
    watt = IntField()
    average = FloatField()
class Temperature(Document):
    timestamp = DateTimeField()
    celsius = IntField()
    average = FloatField()




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wifi")
def wifi():
    wifi = Wifi(timestamp=datetime.datetime.now(), RSSI=420, average=6.9)
    wifi.save()
    print("Wifi entry added: {}".format(wifi.to_json()))
    return render_template("index.html")

@app.route("/power")
def power():
    power = Power(timestamp=datetime.datetime.now(), watt=420, average=6.9)
    power.save()
    print("Power entry added: {}".format(power.to_json()))
    return render_template("index.html")

@app.route("/temperature")
def temperature():
    temperature = Temperature(timestamp=datetime.datetime.now(), celsius=420, average=6.9)
    temperature.save()  # This saves the document to the database
    print("temperature entry added: {}".format(temperature.to_json()))
    return render_template("index.html")

'''
def add_student():
    if(request.method == 'GET'):
        groups = Group.objects.all()
        return render_template("add_student.html", groups=groups)
    else:
        student = Student(firstname=request.form.get("firstname"), lastname=request.form.get("lastname"), birthday=request.form.get("birthday"))
        group = Group(id=request.form.get("groupId"))
        student.group = group
        address = Address(street=request.form.get("street"), city=request.form.get("city"), zip=request.form.get("zip"))
        student.address = address
        student.save()

        groups = Group.objects.all()
        return render_template("add_student.html", groups=groups)


def get_students():
    students = Student.objects.all()
    return render_template("get_students.html", students=students)
'''


app.run(host='0.0.0.0', port=5000)
