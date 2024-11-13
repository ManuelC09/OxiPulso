from flask_mqtt import Mqtt
from threading import Condition
import json

measured_value = None  # Variable global para almacenar el valor medido
mqtt_condition = Condition()  # Variable de condición para sincronizar la espera

def init_mqtt(app, topic):
    mqtt_client = Mqtt(app)
    
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected successfully')
            mqtt_client.subscribe(topic)  # subscribe to topic
        else:
            print(f'Bad connection. Code: {rc}')

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global measured_value
        data = {
            "topic": message.topic,
            "payload": message.payload.decode()
        }
        print(f'Received message on topic: {data["topic"]} with payload: {data["payload"]}')
        
        if data['payload'] == 'medir':
            print('Measurement request received')
        else:
            try:
                measured_value = json.loads(data['payload'])
                with mqtt_condition:
                    mqtt_condition.notify()
            except json.JSONDecodeError:
                print("Error: Payload is not valid JSON")

    return mqtt_client

def wait_for_message(timeout=25):
    global measured_value
    with mqtt_condition:
        mqtt_condition.wait(timeout=timeout)  # Wait for a maximum of `timeout` seconds
    return measured_value
