# UrjaIQ - System Architecture

## High-Level Architecture

```text
                    ┌─────────────────────┐
                    │  Factory Simulator  │
                    │      Python         │
                    └──────────┬──────────┘
                               │
                               │ MQTT
                               ▼
                    ┌─────────────────────┐
                    │   MQTT Broker       │
                    │    Mosquitto        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │   Backend Service   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
          ┌───────────┐ ┌───────────┐ ┌────────────┐
          │PostgreSQL │ │    ML     │ │Optimization│
          │ Database  │ │  Engine   │ │   Engine   │
          └───────────┘ └───────────┘ └────────────┘
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Next.js        │
                    │     Dashboard       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   UrjaIQ Copilot    │
                    │       LLM           │
                    └─────────────────────┘

## Data Flow
Factory Simulator
→ MQTT
→ FastAPI MQTT Consumer
→ Data Validation
→ PostgreSQL
→ Analytics/ML
→ Optimization
→ REST API
→ Next.js Dashboard

Core Services
Simulator

Generates realistic machine and production telemetry.

MQTT

Provides real-time telemetry transport.

Backend

Receives, validates, stores and serves telemetry.

Database

Stores machine, telemetry, production and analytical data.

ML Engine

Performs anomaly detection, health scoring and forecasting.

Optimization Engine

Calculates energy-efficiency opportunities and
simulates optimized scenarios.

Frontend

Provides factory-level and machine-level visualization.

AI Copilot

Converts analytical results into understandable
recommendations and explanations.
```
