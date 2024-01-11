from influxdb_client import Point
from datetime import datetime, timedelta


bucket_influx = "iot_smart_home"
org_influx = "FTN"

#data['name'], data['_time'], alarm_active, data['name'] + ' detected movement.'
def write_alarm_query(write_api, name, time, alarm_status, reason, simulated):
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    value = 0
    if alarm_status:
        value = 1
    
    point = (
        Point('Alarm')
        .tag("simulated", simulated)
        .tag("name", name)
        .tag('timeOfActivation', time)
        .tag('reason', reason)
        .field("measurement", value)
        .time(formatted_time)

    )

    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_dht(write_api, data):
    point = (
        Point(data["measurement_temperature"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value_temperature"])
        .time(data['_time'])

    )

    write_api.write(bucket=bucket_influx, org=org_influx, record=point)
    point = (
        Point(data["measurement_humidity"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value_humidity"])        
        .time(data['_time'])

    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_dms(write_api, data):
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data['_time'])

    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_ds(write_api, data):
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data['_time'])

    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_dus(write_api, data):
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data['_time'])
    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_pir(write_api, data):
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data['_time'])
    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_db(write_api, data):
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data["_time"])
    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_dl(write_api, data):
    if data['value'] == True:
        data['value'] = 1
    elif data['value'] == False:
        data['value'] = 0
    if '_time' in data:
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
            .time(data['_time'])
        )
        write_api.write(bucket=bucket_influx, org=org_influx, record=point)

def write_users_inside(write_api, current_count, action):
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    point = (
        Point('Users')
        .tag('action', action)
        .field("measurement", current_count)
        .time(formatted_time)
    )
    write_api.write(bucket=bucket_influx, org=org_influx, record=point)