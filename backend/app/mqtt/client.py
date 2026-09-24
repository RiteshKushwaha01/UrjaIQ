import json
import logging

import paho.mqtt.client as mqtt
from pydantic import ValidationError

from app.config import settings
from app.database.database import SessionLocal
from app.schemas.telemetry import TelemetryCreate
from app.services.telemetry_service import save_telemetry


logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")

        client.subscribe(
            "urjaiq/factory/telemetry",
            qos=1,
        )

        logger.info(
            "Subscribed to urjaiq/factory/telemetry"
        )
    else:
        logger.error(
            "MQTT connection failed with code %s",
            rc,
        )


def on_message(client, userdata, message):
    db = SessionLocal()

    try:
        payload = json.loads(
            message.payload.decode("utf-8")
        )

        telemetry_data = TelemetryCreate.model_validate(
            payload
        )

        save_telemetry(
            db,
            telemetry_data,
        )

        logger.info(
            "Telemetry stored: machine=%s",
            telemetry_data.machine_id,
        )

    except json.JSONDecodeError:
        logger.error(
            "Invalid JSON received from MQTT"
        )

    except ValidationError as error:
        logger.error(
            "Telemetry validation failed: %s",
            error,
        )

    except Exception:
        logger.exception(
            "Failed to process telemetry message"
        )

    finally:
        db.close()


def create_mqtt_client():
    client = mqtt.Client()

    client.username_pw_set(
        settings.MQTT_USERNAME,
        settings.MQTT_PASSWORD,
    )

    client.tls_set()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(
        settings.MQTT_HOST,
        settings.MQTT_PORT,
        keepalive=60,
    )

    return client