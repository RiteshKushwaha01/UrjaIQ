import json
import random
import time
from datetime import datetime, timezone

from config import MQTT_TOPIC, PUBLISH_INTERVAL
from machines import MACHINES
from mqtt_client import create_mqtt_client


# Current batch production state
current_batch_id = None
current_batch_production = 0
current_batch_good_units = 0
current_batch_rejected_units = 0

# Small, bounded state for each machine.
# This does NOT grow with time.
machine_state = {
    machine["machine_id"]: {
        "degradation": 0.0
    }
    for machine in MACHINES
}


def update_machine_state(machine):
    machine_id = machine["machine_id"]
    state = machine_state[machine_id]

    # Compressor is used to demonstrate gradual degradation.
    if machine_id == "Compressor-01":

        # Small probability of starting degradation.
        if state["degradation"] == 0:
            if random.random() < 0.05:
                state["degradation"] = 0.2

        # Gradually increase degradation.
        elif state["degradation"] < 1.0:
            state["degradation"] += 0.1

        # Recover after reaching severe degradation.
        elif state["degradation"] >= 1.0:
            state["degradation"] = 0.0

    return state["degradation"]


def get_batch_id():
    now = datetime.now(timezone.utc)

    # New production batch every 5 minutes
    batch_minute = (now.minute // 5) * 5

    return (
        f"BATCH-{now.strftime('%Y%m%d-%H')}"
        f"{batch_minute:02d}"
    )


def generate_telemetry(machine, degradation=0.0):
    batch_id = get_batch_id()

    rated_power = machine["rated_power_kw"]

    min_temp, max_temp = machine["temperature_range"]
    min_vibration, max_vibration = machine["vibration_range"]
    min_production, max_production = machine["production_range"]

    # Normal power
    power_kw = random.uniform(
        rated_power * 0.55,
        rated_power * 0.90
    )

    # Machine-specific temperature
    temperature = random.uniform(
        min_temp,
        max_temp
    )

    # Machine-specific vibration
    vibration = random.uniform(
        min_vibration,
        max_vibration
    )

    # Apply degradation gradually
    if degradation > 0:

        power_kw *= 1 + (0.20 * degradation)

        temperature += (
            20 * degradation
        )

        vibration += (
            2.5 * degradation
        )

    voltage = random.uniform(410, 420)

    current = (power_kw * 1000) / voltage

    # Energy consumed during this telemetry interval
    interval_hours = PUBLISH_INTERVAL / 3600

    energy_kwh = power_kw * interval_hours

       # Production is generated once per batch.
    # Only Furnace-01 is the production source.
    global current_batch_id
    global current_batch_production
    global current_batch_good_units
    global current_batch_rejected_units

    if machine["machine_id"] == "Furnace-01":

        if batch_id != current_batch_id:
            current_batch_id = batch_id

            # Generate batch production once
            production_units = random.randint(
                min_production,
                max_production
            )

            # Production decreases with furnace degradation
            production_units = max(
                1,
                int(production_units * (1 - 0.10 * degradation))
            )

            # Quality decreases with degradation
            if degradation > 0.5:
                rejected_units = random.choices(
                    [1, 2, 3],
                    weights=[50, 35, 15]
                )[0]
            else:
                rejected_units = random.choices(
                    [0, 1, 2],
                    weights=[85, 12, 3]
                )[0]

            rejected_units = min(
                rejected_units,
                production_units
            )

            good_units = production_units - rejected_units

            # Store the result for the current batch
            current_batch_production = production_units
            current_batch_good_units = good_units
            current_batch_rejected_units = rejected_units

        else:
            # Reuse the same production result
            production_units = current_batch_production
            good_units = current_batch_good_units
            rejected_units = current_batch_rejected_units

    else:
        # Other machines consume energy but do not produce factory output
        production_units = 0
        good_units = 0
        rejected_units = 0

    if degradation == 0:
        operating_state = "running"
    elif degradation < 0.7:
        operating_state = "warning"
    else:
        operating_state = "degraded"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "batch_id": batch_id,
        "machine_id": machine["machine_id"],
        "machine_type": machine["machine_type"],
        "power_kw": round(power_kw, 2),
        "energy_kwh": round(energy_kwh, 5),
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 2),
        "voltage": round(voltage, 2),
        "current": round(current, 2),
        "operating_state": operating_state,
        "production_units": production_units,
        "good_units": good_units,
        "rejected_units": rejected_units,
    }


def main():
    client = create_mqtt_client()

    print("UrjaIQ Factory Simulator started")
    print(f"Publishing to: {MQTT_TOPIC}")

    try:
        while True:

            for machine in MACHINES:

                degradation = update_machine_state(
                    machine
                )

                telemetry = generate_telemetry(
                    machine,
                    degradation
                )

                payload = json.dumps(
                    telemetry
                )

                client.publish(
                    MQTT_TOPIC,
                    payload
                )

                print(payload)

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()