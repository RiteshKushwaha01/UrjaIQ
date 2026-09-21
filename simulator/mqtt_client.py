import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT


def create_mqtt_client():
    client = mqtt.Client()

    client.connect(
        MQTT_HOST,
        MQTT_PORT,
        keepalive=60,
    )

    return client