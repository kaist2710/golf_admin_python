"""This module has components that are used for testing tuya's device control and Pulsar massage queue."""
import logging
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)
from flask import Flask, request

ACCESS_ID = "p4antwpnfhvvwea9nxcy"
ACCESS_KEY = "7ca0fbf45d4e4f50b7c011aeb5f8ca94"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"

# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init openapi and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Call any API from Tuya
#response = openapi.get("/v1.0/statistics-datas-survey", dict())

# Init Message Queue
# open_pulsar = TuyaOpenPulsar(
#     ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD
# )
# Add Message Queue listener
# open_pulsar.add_message_listener(lambda msg: print(f"---\nexample receive: {msg}"))

# Start Message Queue
# open_pulsar.start()

# input()
# Stop Message Queue
# open_pulsar.stop()

UID = "az16868336961031n8FP"

# Call APIs from Tuya
# Get the device information
# response = openapi.get("/v1.0/iot-03/devices/{}".format(DEVICE_ID))

# # Get the instruction set of the device
# response = openapi.get("/v1.0/iot-03/devices/{}/functions".format(DEVICE_ID))

# # Send commands
# commands = {'commands': [{'code': 'switch_led', 'value': False}]}
# openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)

# # Get the status of a single device
# response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))

# 관리자 정보

app = Flask(__name__)

@app.route('/homes')
def home():
    response = openapi.get("/v1.0/users/{}/homes".format(UID))
    return response

@app.route('/rooms')
def rooms():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    response = openapi.get("/v1.0/homes/{}/rooms".format(request.args['home_id']))
    return response

@app.route('/devices')
def devices():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    response = openapi.get("/v1.0/homes/{}/rooms/{}/devices".format(request.args['home_id'], request.args['room_id']))
    return response

@app.route('/control_power')
def control_power():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'
    
    if request.args['status'] == 'true':
        status = True
    elif request.args['status'] == 'false':
        status = False

    print(status)

    commands = {'commands': [{
        'code': 'switch_1',
        'value': status
    }]}
    print(commands)
    response = openapi.post('/v1.0/devices/{}/commands'.format(request.args['device_id']), commands)
    return response

if __name__ == '__main__':
    app.run(debug=True)