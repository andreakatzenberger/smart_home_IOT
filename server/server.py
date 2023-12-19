from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from influx_writes import *

app = Flask(__name__)


# InfluxDB Configuration
token = "cW5ggpotAfRWPTnrjZe39NBKhetT6JwDnF_TcFGuKbO9nLnZ1bC3mBNMyR-GZ4EvPMH0wO49yqHiS3fZ8e249Q=="
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe("pir")
    client.subscribe("dus")
    client.subscribe("dl")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg.topic, json.loads(msg.payload.decode('utf-8')))


def save_to_db(topic, data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if topic == 'pir':
        point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data['_time'])
        )
        write_api.write(bucket=bucket, org=org, record=point)

    elif topic == 'dus':
        point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data['_time'])
        )
        write_api.write(bucket=bucket, org=org, record=point)



def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")"""
    return handle_influx_query(query)


if __name__ == '__main__':
    app.run(debug=True)
