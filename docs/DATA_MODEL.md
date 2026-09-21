# UrjaIQ - Data Model

## Machine

```text
id
machine_id
name
machine_type
rated_power_kw
status
created_at


## Telemetry
id
timestamp
machine_id
power_kw
energy_kwh
voltage
current
temperature
vibration
operating_state
runtime_minutes


## Production
id
timestamp
production_units
good_units
rejected_units
production_rate

## Alert
id
timestamp
machine_id
alert_type
severity
message
value
threshold
status


## Recommendation
id
timestamp
machine_id
category
title
description
expected_energy_saving
expected_cost_saving
expected_emission_reduction
priority
status


## Optimization Run
id
created_at

baseline_energy_kwh
optimized_energy_kwh

baseline_production
optimized_production

baseline_good_units
optimized_good_units

baseline_rejected_units
optimized_rejected_units

baseline_sec
optimized_sec

baseline_co2e
optimized_co2e


## Important Calculations
Specific Energy Consumption
SEC = Total Energy / Good Units

## Quality Rate
Quality Rate = Good Units / Total Units × 100

## Rejection Rate
Rejection Rate = Rejected Units / Total Units × 100

## Energy Saving
Energy Saving = Baseline Energy - Optimized Energy

## Energy Saving Percentage
Energy Saving % = (Baseline Energy - Optimized Energy) / Baseline Energy × 100

## SEC Improvement
SEC Improvement % = (Baseline SEC - Optimized SEC) / Baseline SEC × 100

## Carbon Intensity
Carbon Intensity = CO2e / Good Units