# UrjaIQ - Project Scope

## 1. Project Name

UrjaIQ

AI-Powered Industrial Energy & Process Optimization Platform

---

## 2. Target Industry

Small and medium-sized metal foundries in India.

The prototype will simulate a small foundry environment.

---

## 3. Problem

SMEs often have limited real-time visibility into machine-level
energy consumption, equipment health, and production efficiency.

This makes it difficult to identify:

- Energy waste
- Abnormal machine behavior
- Equipment degradation
- Inefficient production schedules
- High energy consumption per unit
- Carbon emission reduction opportunities

---

## 4. Solution

UrjaIQ collects simulated machine and production telemetry,
analyzes the data using analytics and machine learning,
identifies inefficiencies and anomalies, and provides
actionable optimization recommendations.

The system follows:

Sense → Understand → Predict → Optimize → Measure

---

## 5. Simulated Machines

1. Furnace-01
2. Compressor-01
3. Motor-01
4. Cooling-01

---

## 6. Core Metrics

### Energy

- Total energy consumption (kWh)
- Power demand (kW)
- Energy cost

### Production

- Total production
- Good units
- Rejected units
- Production rate
- Throughput

### Efficiency

- Specific Energy Consumption (kWh/unit)
- Machine utilization

### Carbon

- CO2e emissions
- CO2e per good unit

### Equipment

- Temperature
- Vibration
- Power
- Health/degradation score

---

## 7. Core Intelligence

### Anomaly Detection

Isolation Forest will identify abnormal machine behavior.

### Machine Health

A degradation-risk score will be calculated from
machine telemetry and historical behavior.

### Energy Forecasting

The system will forecast expected energy consumption.

### Optimization

The system will identify opportunities to reduce energy
consumption while preserving production throughput and quality.

---

## 8. Baseline vs Optimized Scenario

The system must compare:

Baseline:

- Energy
- SEC
- Production
- Quality
- CO2e

Optimized:

- Energy
- SEC
- Production
- Quality
- CO2e

The optimization scenario must preserve throughput and
product quality in the simulation.

---

## 9. AI Copilot

An AI assistant will explain:

- What happened
- Why it happened
- Which machine contributed
- Recommended action
- Expected impact

The AI assistant will consume structured analytical results
rather than directly making numerical predictions from raw data.

---

## 10. Technology Stack

Frontend:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Recharts

Backend:

- Python
- FastAPI
- SQLAlchemy
- Pydantic

Database:

- PostgreSQL

IoT:

- MQTT
- Eclipse Mosquitto

Simulation:

- Python
- NumPy
- Pandas
- Paho MQTT

Machine Learning:

- Scikit-learn
- XGBoost if required

AI:

- LLM API

Infrastructure:

- Docker
- Docker Compose

Version Control:

- Git
- GitHub

---

## 11. Prototype Principle

The backend must work independently of the telemetry source.

The telemetry producer can be:

1. Factory simulator
2. Future physical IoT hardware

Both should use the same MQTT message format.

---

## 12. Primary Demo

The final demonstration will show:

Factory telemetry
→ Real-time monitoring
→ Anomaly detection
→ Machine health
→ Energy inefficiency
→ Optimization recommendation
→ Baseline vs optimized simulation
→ Reduced SEC and emissions
→ Throughput and quality preserved
