import threading
import time

from flask import Flask, jsonify, request, render_template
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from influx_writes import *
import paho.mqtt.publish as publish
import schedule
from threading import Lock
from flask_socketio import SocketIO
from flask_cors import CORS
app = Flask(__name__)
mqtt_client = mqtt.Client()
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    #socketio.emit('message_from_server', 'Hello from the server!', namespace='/')
    #send_message_to_client(msg)

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected')

def send_message_to_client(message):
    # Make sure to use the same namespace if specified
    socketio.emit('message_from_server', message, namespace='/')


# InfluxDB Configuration
users_inside = 0
alarm_active = False
system_active = False
alarm_active_button = False
schedule_safety = False
clock_active = False
pin_lock = Lock()
schedule_lock = Lock()
system_lock = Lock()
alarm_lock = Lock()
users_lock = Lock()
alarm_active_button_lock = Lock()
current_pin = ''
token = "nIMmUKQlkBAmDplXVdIowNLj-xCNJXlpGvMWioTMJ7-G5O-n8-Sec94eSZsiExMGJGXApEm4ro7Z6xKRhoDE_w=="
org = "FTN"
url = "http://localhost:8086"
bucket = "iot_smart_home"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)
HOSTNAME = "localhost"
PORT = 1883
scheduled = False
# MQTT Configuration

def on_connect(client, userdata, flags, rc):

    client.subscribe("dht", qos=1)
    client.subscribe("dms", qos=1)
    client.subscribe("ds", qos=1)
    client.subscribe("dus", qos=1)
    client.subscribe("pir", qos=1)
    client.subscribe("db", qos=1)
    client.subscribe("dl", qos=1)
    client.subscribe("lcd", qos=1)
    client.subscribe("gsg", qos=1)
    client.subscribe("b4sd", qos=1)
    client.subscribe('alarm-on-server', qos=1)
    client.subscribe('dms-entered-pin', qos=1)
    client.subscribe('bir', qos=1)
    client.subscribe('rgb', qos=1)
    



def save_to_db(topic, data):
    global users_inside
    global alarm_active
    global  alarm_active_button
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if topic == 'dht':

        if data['name'] == 'GDHT':
            dht_message = "humidity: " + str(data["value_humidity"]) + "\n" + "temperature: " + str(data["value_temperature"])

            publish.single('dht-lcd-display', json.dumps({'temperature':dht_message}), hostname=HOSTNAME, port=PORT)
        write_dht(write_api, data)
    elif topic == 'dms':
        write_dms(write_api, data)
    elif topic == 'ds':
        if 'alarm' in data and data['alarm'] == True:
            with alarm_active_button_lock:
                if alarm_active_button != True:
                    mqtt_client.publish('alarm-on', json.dumps({'':''}), qos=1)
                    with alarm_lock:
                        alarm_active = True
                        print(topic)
                        send_message_to_client(alarm_active)

                        alarm_active_button = True
                        write_alarm_query(write_api, data['name'], data['_time'], alarm_active,
                                      "Button is not pressed for more than 5 seconds", data['simulated'])
        elif data['alarm'] is not None and data['alarm'] == False:
            with alarm_active_button_lock:
                if alarm_active_button != False:

                    mqtt_client.publish('alarm-off', json.dumps({'':''}), qos=1)
                    with alarm_lock:
                        alarm_active = False
                        send_message_to_client(alarm_active)
                        alarm_active_button = False
                        write_alarm_query(write_api, data['name'], data['_time'], alarm_active,
                                          "Button is not pressed anymore", data['simulated'])
        write_ds(write_api, data)
    elif topic == 'dus':
        write_dus(write_api, data)
    elif topic == 'pir':
        if 'RPIR' in data['name']:
            write_pir(write_api, data)
            with users_lock:
                if users_inside == 0:
                    with alarm_lock:
                        alarm_active = True
                        print(topic)
                        send_message_to_client(alarm_active)

                        mqtt_client.publish('alarm-on', json.dumps({'':''}), qos=1)
                        write_alarm_query(write_api, data['name'], data['_time'], alarm_active, data['name'] + ' detected movement.', data['simulated'])
            return
        query_data = []
        if data['name'] == 'DPIR1':
            query = f"""from(bucket: "{bucket}")
            |> range(start: -40s)
            |> filter(fn: (r) => r._measurement == "Distance")
            |> filter(fn: (r) => r["name"] == "DUS1")
            |> sort(columns: ["_time"], desc: true)
            |> limit(n: 3)"""
            # print(query)
            query_data = handle_influx_query(query)
            # print("\n",query_data)
            publish.single('dpir1-light-on', json.dumps({'light':'on'}), hostname=HOSTNAME, port=PORT)
        elif data['name'] == 'DPIR2':
            query = f"""from(bucket: "{bucket}")
            |> range(start: -40s)
            |> filter(fn: (r) => r._measurement == "Distance")
            |> filter(fn: (r) => r["name"] == "DUS2")
            |> sort(columns: ["_time"], desc: true)
            |> limit(n: 3)"""
            query_data = handle_influx_query(query)
        is_entering = False
        if len(query_data['data']) > 2:
            if query_data['data'][0]['_value'] > query_data['data'][2]['_value']:
                is_entering = True
            if is_entering:
                with users_lock:
                    users_inside += 1
                    write_users_inside(write_api, users_inside, 'user entered')

            else:
                with users_lock:
                    users_inside -= 1
                    if users_inside < 0:
                        users_inside = 0
                    write_users_inside(write_api, users_inside, 'user left')
        with users_lock:
            if users_inside < 0:
                users_inside = 0
        write_pir(write_api, data)
    elif topic == 'db':
        write_db(write_api, data)
    elif topic == 'dl':
        write_dl(write_api, data)
    elif topic == 'gsg':
        if data['suspicious'] is not None and data['suspicious'] == True:
            with alarm_lock:
                alarm_active = True
                print(topic)
                send_message_to_client(alarm_active)

                mqtt_client.publish('alarm-on', json.dumps({'':''}), qos=1)
                write_alarm_query(write_api, data['name'], data['_time'], alarm_active, data['name'] + ' detected unusual values.', data['simulated'])
        write_db(write_api, data)
    elif topic == 'lcd' or topic == 'b4sd':
        write_db(write_api, data)
    elif topic == 'alarm-on-server':
        with alarm_lock:
            alarm_active = True
            print(topic)
            send_message_to_client(alarm_active)
        mqtt_client.publish('alarm-on', json.dumps({'':''}), qos=1)
    elif topic == 'dms-entered-pin':
        global current_pin, schedule_safety, system_active
        with system_lock:
            if not system_active:
                with pin_lock:
                    with schedule_lock:
                        current_pin = data['pin'][0:4]
                        threading.Thread(target=run_schedule, daemon=True).start()
            else:
                with pin_lock:
                    with system_lock:
                        with alarm_lock:
                            if current_pin == data['pin'][0:4]:
                                system_active = False
                                alarm_active = False
                                send_message_to_client(alarm_active)

                                publish.single('system-off', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)
                                publish.single('alarm-off', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)
    elif topic == 'bir':
        write_db(write_api, data)
    elif topic == 'rgb':
        if data['measurement'] != 'Light':
            write_db(write_api, data)

def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return {"status": "success", "data": container}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/measurement/<string:name>/<string:devicename>', methods=['GET'])
def get_last_measurement_data(name, devicename):

    if name == 'dht':
        values = []
        query = f"""from(bucket: "{bucket}")
        |> range(start: -25m)
        |> filter(fn: (r) => r._measurement == "Temperature")
        |> filter(fn: (r) => r["name"] == "{devicename}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 1)
        """
        temperature = handle_influx_query(query)
        if 'error' not in temperature:
            if len(temperature['data']) > 0:
                values.append(temperature['data'][0])
        query = f"""from(bucket: "{bucket}")
        |> range(start: -25m)
        |> filter(fn: (r) => r._measurement == "Humidity")
        |> filter(fn: (r) => r["name"] == "{devicename}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 1)
        """
        humidity = handle_influx_query(query)
        if 'error' not in humidity:
            if len(humidity['data']) > 0:
                values.append(humidity['data'][0])
        return values

    elif name == 'gyro':
        values = []
        query = f"""from(bucket: "{bucket}")
        |> range(start: -25m)
        |> filter(fn: (r) => r._measurement == "Accelerator")
        |> filter(fn: (r) => r["name"] == "{devicename}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 1)
        """
        accelerator = handle_influx_query(query)
        if 'error' not in accelerator:
            if len(accelerator['data']) > 0:
                values.append(accelerator['data'][0])
        query = f"""from(bucket: "{bucket}")
        |> range(start: -25m)
        |> filter(fn: (r) => r._measurement == "Gyroscope")
        |> filter(fn: (r) => r["name"] == "{devicename}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 1)
        """
        gyroscope = handle_influx_query(query)
        if 'error' not in gyroscope:
            if len(gyroscope['data']) > 0:
                values.append(gyroscope['data'][0])
        
        return values

    else:
        query = f"""from(bucket: "{bucket}")
        |> range(start: -25m)
        |> filter(fn: (r) => r._measurement == "{name}")
        |> filter(fn: (r) => r["name"] == "{devicename}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 1)
        """
        values = handle_influx_query(query)
        if 'error' not in values:
            if len(values['data']) > 0:
                return values['data']
            return []
        else:
            return values['message']


@app.route('/rgb/<string:button_pressed>', methods=['PUT'])
def set_rgb_color(button_pressed):
    publish.single('bir-button-pressed', json.dumps({'button': button_pressed}), hostname=HOSTNAME, port=PORT)
    return {"status": "success"}


def run_schedule():
    global current_pin, schedule_safety, system_active
    with schedule_lock:
        schedule_safety = True
    time.sleep(10)
    publish.single('system-on', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)

    with schedule_lock:
        schedule_safety = False
    with system_lock:
        system_active = True

@app.route('/set_system_pin/<string:pin>', methods=['PUT'])
def activate_safety_system(pin):
    global current_pin, schedule_safety, system_active

    if '#' in pin:
        if len(pin) != 5:
            return json.dumps({'error': 'Pin should have 4 characters + #'})
    else:
        if len(pin) != 4:
            return json.dumps({'error': 'Pin should have 4 characters'})
    with pin_lock:
        current_pin = pin[0:4]
    with system_lock:
        if system_active is True:
            return json.dumps({'error': 'Safety system is already active'})
    with schedule_lock:
        if schedule_safety is True:
            return json.dumps({'error': 'Safety system scheduling in progress'})

    threading.Thread(target=run_schedule, daemon=True).start()
    return json.dumps({'response': 'Alarm successfully activated'})

@app.route('/deactivate-safety-system/<string:pin>', methods=['PUT'])
def deactivate_safety_system(pin):
    global current_pin, system_active, alarm_active

    with system_lock:
        if system_active is False:
            return json.dumps({'error': 'System is not active'})

    if '#' in pin:
        if len(pin) != 5:
            return json.dumps({'error': 'Pin should have 4 characters + #'})
    else:
        if len(pin) != 4:
            return json.dumps({'error': 'Pin should have 4 characters'})

    with pin_lock:
        if current_pin != pin[0:4]:
            return json.dumps({'error': 'Incorrect pin. Try again'})
    with system_lock:
        system_active = False
    with alarm_lock:
        alarm_active = False
        send_message_to_client(alarm_active)

    publish.single('system-off', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)
    publish.single('alarm-off', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)

    return json.dumps({'response': 'Alarm successfully deactivated.'})

def activate_alarm():
    global clock_active, scheduled
    clock_active = True

    scheduled = False
    publish.single('clock-activate', json.dumps({'clock':'on'}), hostname=HOSTNAME, port=PORT)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global scheduled
    try:
        data = request.get_json()
        alarm_time = data.get("alarm_time")
        print(f"Postavljen alarm za: {alarm_time}")

        if not scheduled:
            alarm_time_obj = datetime.strptime(alarm_time, "%H:%M").time()
            print(alarm_time_obj.strftime("%H:%M"))
            schedule.every().day.at(alarm_time_obj.strftime("%H:%M")).do(activate_alarm)
            scheduled = True
        def run_schedule():
            while scheduled is True:
                schedule.run_pending()
                time.sleep(1)
        threading.Thread(target=run_schedule, daemon=True).start()

        return jsonify({"message": "Alarm set successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    global clock_active
    try:

        publish.single('clock-stop', json.dumps({'clock': 'off'}), hostname=HOSTNAME, port=PORT)
        clock_active = False
        return jsonify({"message": "Clock stopped successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_alarm_status', methods=['GET'])
def get_alarm_status():
    global alarm_active
    with alarm_lock:
        return json.dumps({'status': alarm_active})

@app.route('/deactivate-system_alarm', methods=['PUT'])
def deactivate_system_alarm():
    global alarm_active

    with alarm_lock:
        alarm_active = False
        send_message_to_client(alarm_active)
        publish.single('alarm-off', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)
    return json.dumps({'response': 'Alarm successfully deactivated.'})


if __name__ == '__main__':
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg.topic, json.loads(msg.payload.decode('utf-8')))
    socketio.init_app(app)
    socketio.run(app, debug=False)

