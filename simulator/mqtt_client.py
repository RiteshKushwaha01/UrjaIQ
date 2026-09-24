import paho.mqtt.client as mqtt

from config import (
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)


def create_mqtt_client():
    client = mqtt.Client()

    client.username_pw_set(
        MQTT_USERNAME,
        MQTT_PASSWORD,
    )

    client.tls_set()

    client.connect(
        MQTT_HOST,
        MQTT_PORT,
        keepalive=60,
    )

    return client