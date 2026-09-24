# UrjaIQ ⚡

### AI-Powered Industrial Energy & Process Optimization Platform for Indian SME Manufacturing

> **Sense → Understand → Predict → Optimize → Measure**

UrjaIQ is an AI-powered industrial intelligence platform designed to help **small and medium-sized manufacturing enterprises (SMEs)** monitor energy consumption in real time, understand machine performance, detect abnormal operating behavior, identify energy-intensive equipment, optimize processes, and measure carbon impact.

The platform combines **IoT telemetry, real-time analytics, machine learning, optimization algorithms, carbon accounting, and an AI Copilot** into a single factory intelligence dashboard.

---

## 📌 Table of Contents

- [About UrjaIQ](#-about-urjaiq)
- [The Problem](#-the-problem)
- [Why This Problem Matters](#-why-this-problem-matters)
- [Our Solution](#-our-solution)
- [How UrjaIQ Works](#-how-urjaiq-works)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Why These Technologies](#-why-these-technologies)
- [Data Flow](#-data-flow)
- [Machine Intelligence](#-machine-intelligence)
- [Energy Optimization](#-energy-optimization)
- [Carbon Accounting](#-carbon-accounting)
- [AI Copilot](#-ai-copilot)
- [Factory KPIs](#-factory-kpis)
- [Prototype & Simulation](#-prototype--simulation)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Overview](#-api-overview)
- [Example Telemetry](#-example-telemetry)
- [Example Results](#-example-results)
- [Business & Deployment Model](#-business--deployment-model)
- [Limitations](#-current-limitations)
- [Future Scope](#-future-scope)
- [Security Considerations](#-security-considerations)
- [Design Philosophy](#-design-philosophy)
- [Alignment With the Challenge](#-alignment-with-the-challenge)
- [Development](#-development)
- [License](#-license)
- [Team](#-team)
- [Final Message](#-final-message)

---

# 🚀 About UrjaIQ

Industrial SMEs often operate with limited visibility into **where energy is being consumed, which machines are responsible, whether equipment is behaving abnormally, and how energy consumption relates to production output**.

UrjaIQ addresses this gap by creating a digital intelligence layer for the factory.

Instead of looking at electricity consumption as a single monthly bill, UrjaIQ connects:

```text
Energy
   +
Machine Health
   +
Production
   +
Quality
   +
Carbon
   +
AI
```

to provide a unified view of factory performance.

The platform is currently demonstrated using a **simulated small metal-foundry environment**, allowing the complete software pipeline to be tested without requiring physical industrial hardware.

---

# ❗ The Problem

The official challenge focuses on:

> **Smart Manufacturing — Industrial Energy & Process Efficiency**

with the objective of bringing affordable real-time energy monitoring, predictive maintenance and process optimisation to Indian SMEs.

Many small and medium-sized factories face several interconnected problems.

### 1. Limited real-time energy visibility

Factories may know their total electricity consumption but not necessarily:

- Which machine consumes the most energy?
- When does energy consumption increase?
- How much energy is consumed during idle periods?
- How does energy consumption change between production batches?

Without machine-level visibility, identifying energy waste becomes difficult.

### 2. Energy is directly connected to production cost

For energy-intensive manufacturing, energy can represent a significant portion of production costs.

The challenge statement notes that energy can account for **15–30% of production costs** in energy-intensive businesses.

Therefore, reducing unnecessary energy consumption can directly improve operating economics.

### 3. Machine problems can increase energy consumption

A machine does not necessarily have to completely fail before becoming inefficient.

Changes in:

- temperature
- vibration
- power
- voltage
- current

can indicate unusual operating behavior.

Early identification can help maintenance teams investigate before the problem becomes more serious.

### 4. Energy efficiency cannot come at the cost of production

Simply reducing machine power is not a valid optimization strategy if it causes:

- lower production
- increased rejection
- reduced quality
- longer production cycles

Therefore, UrjaIQ evaluates energy consumption alongside production and quality.

### 5. Carbon visibility

Manufacturers increasingly need to understand their environmental impact.

UrjaIQ converts energy consumption into estimated:

```text
Energy consumption
        ↓
CO₂e emissions
        ↓
CO₂e per good unit
```

This creates a simple foundation for carbon monitoring and future sustainability reporting.

---

# 🎯 Why UrjaIQ Is Required

The challenge specifically calls for solutions that can:

- reduce specific energy consumption
- provide real-time visibility
- support decarbonisation
- strengthen SME competitiveness
- remain economically viable for SMEs with limited capital and technical resources.

UrjaIQ therefore focuses on **actionable intelligence rather than simply displaying sensor values**.

The core idea is:

```text
Raw Sensor Data
      ↓
Real-Time Monitoring
      ↓
Analytics
      ↓
Machine Intelligence
      ↓
Optimization Recommendations
      ↓
Measured Impact
```

---

# 💡 Our Solution

UrjaIQ provides a unified factory intelligence platform consisting of six major layers:

### 1. Sense

Collect machine telemetry such as:

- power
- energy
- voltage
- current
- temperature
- vibration
- operating state

### 2. Understand

Calculate:

- total factory energy
- machine energy consumption
- peak power
- production
- good units
- rejected units
- quality rate
- specific energy consumption

### 3. Predict / Detect

Use machine learning to identify unusual machine behavior.

The prototype currently uses **Isolation Forest anomaly detection**.

### 4. Optimize

Identify machines consuming a large share of factory energy and generate optimization recommendations.

### 5. Measure

Calculate:

- energy savings
- SEC improvement
- cost savings
- CO₂e reduction estimates

### 6. Explain

The AI Copilot converts factory analytics into natural-language answers for plant managers.

---

# 🏭 Target Use Case

The prototype models a **small metal foundry**.

The simulated factory contains:

| Machine | Type |
|---|---|
| Furnace-01 | Melting Furnace |
| Compressor-01 | Air Compressor |
| Motor-01 | Industrial Motor |
| Cooling-01 | Cooling System |

The architecture is designed so that the same approach can later be adapted to:

- foundries
- textile manufacturing
- ceramics
- chemicals
- food processing
- brick kilns

These are among the industrial contexts highlighted by the challenge.

---

# ⚙️ Key Features

## 📊 Real-Time Factory Monitoring

Monitor machine-level telemetry in real time.

Metrics include:

- Power (kW)
- Energy (kWh)
- Temperature
- Vibration
- Voltage
- Current
- Operating state

---

## 📈 Production Analytics

UrjaIQ connects energy with production.

It tracks:

- Total production
- Good units
- Rejected units
- Quality rate
- Batch performance
- Energy per good unit

This prevents optimization from becoming simply "use less electricity."

---

## ⚡ Specific Energy Consumption

A central KPI is:

```text
SEC = Total Energy Consumption / Good Production Units
```

For example:

```text
Factory Energy = 489.5691 kWh
Good Units     = 352

SEC = 489.5691 / 352
    ≈ 1.3908 kWh/good unit
```

This gives a more meaningful efficiency measurement than total electricity consumption alone.

---

# 🤖 Machine Learning Anomaly Detection

UrjaIQ uses **Isolation Forest** to identify unusual machine behavior.

The model considers features such as:

```text
Power
Temperature
Vibration
Voltage
Current
```

The system identifies telemetry patterns that differ significantly from normal operating behavior.

### Important distinction

An anomaly does **not** automatically mean that a machine will fail.

Instead:

```text
Anomaly
   ↓
Unusual behavior detected
   ↓
Operator investigation
   ↓
Potential maintenance action
```

This makes the current prototype's ML capability appropriately focused on **anomaly detection**, rather than claiming unsupported failure prediction.

---

# ⚡ Energy Optimization

UrjaIQ calculates the energy contribution of individual machines.

For example:

```text
Factory Energy
       │
       ├── Furnace-01       39.6%
       ├── Compressor-01    25.8%
       ├── Cooling-01       ...
       └── Motor-01         ...
```

Machines consuming a larger proportion of factory energy receive higher-priority recommendations.

Example:

> Furnace-01 accounts for approximately 40% of factory energy consumption. Review operating and idle periods for energy-saving opportunities without reducing production output or quality.

The recommendations are **decision-support suggestions**, not automatic machine-control commands.

---

# 📉 Simulated Optimization Scenario

The prototype includes an optimization scenario using an **8% estimated energy reduction assumption**.

The system calculates:

```text
Baseline Energy
       ↓
Estimated Reduction
       ↓
Optimized Energy
       ↓
SEC Improvement
       ↓
Estimated Cost Saving
```

This allows the prototype to demonstrate how an SME could evaluate an optimization opportunity.

The 8% value is a **simulation assumption**, not a measured industrial result.

---

# 🌱 Carbon Accounting

UrjaIQ estimates carbon emissions from electricity consumption.

Prototype formula:

```text
CO₂e = Energy Consumption × Emission Factor
```

Current prototype emission factor:

```text
0.70 kg CO₂e / kWh
```

It also calculates:

```text
CO₂e per good unit
```

This enables the factory to view both:

- absolute estimated emissions
- production-normalized emissions

The emission factor is configurable and should be replaced with an appropriate regional/grid or organizational factor for real deployment.

---

# 🧠 AI Copilot

UrjaIQ includes an AI Copilot powered by Google's Gemini API.

The Copilot does **not** independently invent factory statistics.

Instead:

```text
PostgreSQL
     ↓
Validated Analytics
     ↓
Factory Context
     ↓
Gemini
     ↓
Natural Language Explanation
```

This allows a factory manager to ask questions such as:

```text
What is the current energy situation?

Which machine consumes the most energy?

Are there any machine anomalies?

What is our specific energy consumption?

What are the main optimization opportunities?

What is our estimated carbon footprint?
```

The AI is instructed to:

- use actual factory numbers
- avoid inventing values
- identify when data is unavailable
- distinguish anomalies from confirmed failures
- treat carbon values as estimates
- treat optimization opportunities as recommendations

---

# 🏗️ System Architecture

```text
                  ┌──────────────────────┐
                  │ Factory Simulator    │
                  │ Python + NumPy       │
                  └──────────┬───────────┘
                             │
                             │ MQTT
                             ▼
                  ┌──────────────────────┐
                  │ Mosquitto Broker     │
                  │ MQTT                 │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ FastAPI Backend      │
                  │ REST APIs            │
                  └──────────┬───────────┘
                             │
                 ┌───────────┴────────────┐
                 ▼                        ▼
       ┌──────────────────┐      ┌──────────────────┐
       │ PostgreSQL       │      │ ML Engine        │
       │ Factory Data     │      │ Anomaly Detection│
       └──────────────────┘      └──────────────────┘
                 │                        │
                 └───────────┬────────────┘
                             ▼
                  ┌──────────────────────┐
                  │ Analytics &          │
                  │ Optimization Engine  │
                  └──────────┬───────────┘
                             │
                    ┌────────┴─────────┐
                    ▼                  ▼
          ┌─────────────────┐   ┌────────────────┐
          │ Next.js         │   │ AI Copilot     │
          │ Dashboard       │   │ Gemini API     │
          └─────────────────┘   └────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| Next.js | Dashboard application |
| React | UI components |
| TypeScript | Type-safe frontend development |
| Tailwind CSS | Responsive UI styling |
| Recharts / Charts | Data visualization |

## Backend

| Technology | Purpose |
|---|---|
| Python | Backend and data processing |
| FastAPI | REST API |
| SQLAlchemy | Database ORM |
| Pydantic | Request/data validation |
| PostgreSQL | Persistent telemetry storage |

## IoT / Data Pipeline

| Technology | Purpose |
|---|---|
| MQTT | Lightweight telemetry communication |
| Mosquitto | MQTT broker |
| Paho MQTT | Python MQTT client |
| NumPy | Simulation/data generation |
| Pandas | Data processing |

## Machine Learning

| Technology | Purpose |
|---|---|
| Scikit-learn | ML framework |
| Isolation Forest | Anomaly detection |

## AI

| Technology | Purpose |
|---|---|
| Gemini API | Natural-language factory Copilot |

## Infrastructure

| Technology | Purpose |
|---|---|
| Docker | Infrastructure isolation |
| Docker Compose | Local multi-service orchestration |
| Git | Version control |
| GitHub | Source-code hosting |

---

# 🤔 Why These Technologies?

## Why MQTT?

Industrial telemetry can consist of frequent small messages.

MQTT is suitable because it provides a lightweight publish/subscribe communication model:

```text
Factory Device
     ↓
 MQTT Topic
     ↓
Broker
     ↓
Backend
```

It also keeps the telemetry layer decoupled from the application layer.

---

## Why FastAPI?

FastAPI provides:

- Python-native development
- automatic OpenAPI documentation
- Pydantic validation
- asynchronous capabilities
- straightforward REST API development

It also integrates naturally with the Python-based ML pipeline.

---

## Why PostgreSQL?

Factory telemetry is structured and relational.

PostgreSQL provides a reliable foundation for:

- telemetry
- machines
- batches
- production
- analytics
- recommendations
- optimization results

It also supports efficient SQL aggregation for factory KPIs.

---

## Why Isolation Forest?

The prototype does not have a large historical dataset containing confirmed machine failures.

Therefore, supervised failure prediction would require assumptions that the current data cannot properly support.

Isolation Forest allows us to detect **unusual operating patterns without requiring labeled failure data**.

---

## Why Next.js?

Next.js provides a modern React-based application framework suitable for building the interactive factory dashboard.

It supports:

- component-based UI
- efficient frontend architecture
- TypeScript
- production builds
- scalable application structure

---

## Why Gemini?

The core factory calculations are performed by the application.

Gemini is used primarily as an **explanation and interaction layer**.

This separation is important:

```text
Application
→ calculates the truth

AI
→ explains the truth
```

This reduces the risk of using an LLM as the primary numerical calculation engine.

---

# 🔄 Data Flow

A telemetry message follows this path:

```text
1. Simulator generates telemetry

        ↓

2. MQTT publishes message

        ↓

3. Mosquitto receives message

        ↓

4. FastAPI MQTT client consumes message

        ↓

5. Pydantic validates telemetry

        ↓

6. PostgreSQL stores telemetry

        ↓

7. Analytics engine processes data

        ↓

8. ML engine detects anomalies

        ↓

9. Optimization engine identifies opportunities

        ↓

10. Next.js dashboard visualizes results

        ↓

11. AI Copilot explains the results
```

---

# 📡 Telemetry Model

Each telemetry event contains information such as:

```json
{
  "timestamp": "2026-09-24T06:56:21+00:00",
  "batch_id": "BATCH-20260924-0655",
  "machine_id": "Furnace-01",
  "machine_type": "melting_furnace",
  "power_kw": 91.62,
  "energy_kwh": 0.0509,
  "temperature": 718.9,
  "vibration": 1.63,
  "voltage": 415.61,
  "current": 220.45,
  "operating_state": "running",
  "production_units": 10,
  "good_units": 10,
  "rejected_units": 0
}
```

---

# 📊 Factory KPIs

UrjaIQ currently calculates:

### Energy

```text
Total Energy
Peak Power
Machine Energy
Machine Energy Share
```

### Production

```text
Production Units
Good Units
Rejected Units
Quality Rate
```

### Efficiency

```text
Specific Energy Consumption
```

### Carbon

```text
Estimated CO₂e
CO₂e / Good Unit
```

### Machine Intelligence

```text
Anomaly Status
Anomaly Score
Machine Health Indicators
```

---

# 🧪 Prototype & Simulation

No physical hardware is required for the prototype.

The challenge explicitly states that a software prototype or simulation is encouraged and that physical hardware is not expected.

UrjaIQ therefore includes a Python-based factory simulator that generates realistic-looking telemetry for the four machines.

The simulator allows the complete architecture to be demonstrated:

- continuous telemetry
- machine-level energy consumption
- batch production
- quality variation
- machine parameters
- anomaly detection
- energy analytics
- optimization
- carbon accounting

### Why simulation?

It allows the complete architecture to be tested before connecting physical industrial equipment.

In a production deployment:

```text
Simulator
      ↓
Smart Meter / Sensor / PLC
```

The rest of the architecture can remain conceptually similar.

---

# 📁 Project Structure

```text
UrjaIQ/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── telemetry.py
│       │   ├── analytics.py
│       │   ├── ml.py
│       │   ├── optimization.py
│       │   ├── carbon.py
│       │   └── ai.py
│       │
│       ├── database/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       ├── mqtt/
│       ├── ml/
│       └── main.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/
│
├── simulator/
│   └── simulator.py
│
├── database/
│
├── docker/
│
├── docs/
│   ├── PROJECT_SCOPE.md
│   ├── ARCHITECTURE.md
│   └── DATA_MODEL.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Install:

- Git
- Docker Desktop
- Python 3.11+
- Node.js 20+
- npm

---

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd UrjaIQ
```

---

## 2. Start Infrastructure

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

You should have:

```text
PostgreSQL
Mosquitto
```

running.

---

# 3. Configure Environment Variables

Create:

```text
.env
```

Example:

```env
POSTGRES_USER=urjaiq
POSTGRES_PASSWORD=urjaiq_password
POSTGRES_DB=urjaiq_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

MQTT_HOST=localhost
MQTT_PORT=1883

GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.5-flash
```

### ⚠️ Security

Never commit `.env` to GitHub.

Use:

```text
.env.example
```

for sharing configuration structure.

---

# 4. Start Backend

```bash
cd backend
source .venv/Scripts/activate
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# 5. Start Simulator

Open another terminal:

```bash
cd simulator
source .venv/Scripts/activate
python simulator.py
```

You should see:

```text
UrjaIQ Factory Simulator started
Publishing to: urjaiq/factory/telemetry
```

---

# 6. Start Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the URL shown by Next.js, usually:

```text
http://localhost:3000
```

---

# 🔌 API Overview

| Endpoint | Purpose |
|---|---|
| `/api/telemetry/...` | Telemetry and machine data |
| `/api/analytics/overview` | Factory analytics |
| `/api/ml/...` | ML anomaly detection |
| `/api/optimization/baseline` | Baseline efficiency |
| `/api/optimization/machine-energy` | Machine energy distribution |
| `/api/optimization/recommendations` | Optimization recommendations |
| `/api/optimization/savings` | Simulated savings |
| `/api/carbon/overview` | Carbon metrics |
| `/api/ai/chat` | AI Copilot |

---

# 📈 Example Prototype Results

At one verified point during development, UrjaIQ reported:

```text
Analyzed batches       : 27
Factory energy         : 489.5691 kWh
Peak power             : 108.0 kW
Production             : 360 units
Good units             : 352
Rejected units         : 8
Quality rate           : 97.78%
SEC                    : 1.3908 kWh/good unit
Estimated CO₂e         : 342.6984 kg
CO₂e / good unit       : 0.9736 kg
```

These are **simulation results**, not measurements from a physical factory.

Because the simulator continuously generates new telemetry, dashboard values change over time.

---

# 💼 Business & Deployment Model

UrjaIQ is designed around a potential **SME-friendly industrial SaaS + monitoring model**.

### Target customers

- Small foundries
- Textile units
- Ceramic manufacturers
- Food processing units
- Chemical manufacturers
- Other energy-intensive SMEs

### Potential deployment

```text
Smart Meters
     +
Machine Sensors
     +
PLC / Industrial Gateway
          ↓
      Edge Gateway
          ↓
       MQTT
          ↓
       UrjaIQ
          ↓
 Dashboard + AI
```

The initial prototype uses simulation, while production deployment would require integration with actual meters, PLCs, sensors and plant systems.

---

# 💰 Potential Value Proposition

UrjaIQ aims to help factories answer:

> **Where is energy being consumed?**

> **Why is it being consumed?**

> **Which machine should we investigate first?**

> **Is the machine behaving unusually?**

> **How much energy could potentially be saved?**

> **What is the carbon impact?**

> **How does energy consumption relate to production quality?**

This turns factory energy data into an operational decision-support system.

---

# ⚠️ Current Limitations

UrjaIQ is currently a prototype/simulation.

Therefore:

### 1. Telemetry is simulated

The current data does not originate from physical industrial sensors.

### 2. Anomaly detection is not failure prediction

Isolation Forest detects unusual patterns but does not prove that a machine will fail.

### 3. Optimization savings are simulated

The current optimization scenario uses an assumed reduction percentage to demonstrate the calculation workflow.

### 4. Carbon factor is configurable

The prototype currently uses:

```text
0.70 kg CO₂e/kWh
```

A production deployment should use an appropriate verified emission factor.

### 5. AI depends on an external LLM

Gemini availability, rate limits and API access can affect Copilot availability.

---

# 🔮 Future Scope

## Hardware Integration

Connect:

- smart energy meters
- vibration sensors
- temperature sensors
- PLCs
- industrial gateways

---

## Advanced Predictive Maintenance

With historical failure data:

```text
Sensor Data
     ↓
Feature Engineering
     ↓
Failure Prediction
     ↓
Remaining Useful Life
     ↓
Maintenance Planning
```

---

## Production Scheduling

Future optimization could consider:

- electricity tariff
- peak demand
- machine availability
- production deadlines
- renewable energy availability

to recommend more efficient production schedules.

---

## Renewable Energy Integration

The system can eventually incorporate:

- rooftop solar
- battery storage
- grid electricity
- renewable generation forecasts

into the optimization engine.

---

## Digital Energy Audit

Future versions can automatically generate:

```text
Energy Baseline
      ↓
Machine Benchmark
      ↓
Waste Identification
      ↓
Retrofit Opportunities
      ↓
Priority Roadmap
```

---

## Enterprise Integration

Future integrations could include:

- ERP
- MES
- SCADA
- BMS
- procurement systems
- production management systems

---

# 🔐 Security Considerations

For the prototype:

- API keys are stored in `.env`
- `.env` is excluded from Git
- API request validation uses Pydantic
- Database access is centralized
- MQTT is isolated through Docker

For production deployment, additional security would be required:

- MQTT authentication
- TLS
- encrypted database connections
- role-based access control
- API authentication
- secret management
- network segmentation
- audit logging
- secure edge gateways

---

# 🎯 Design Philosophy

UrjaIQ follows five principles:

### 1. Affordable

Designed with technologies that can support a lower-cost SME deployment.

### 2. Actionable

Don't just show data — identify what deserves attention.

### 3. Production-aware

Energy efficiency should not come at the cost of throughput or quality.

### 4. Explainable

Factory managers should understand why a machine or process is being highlighted.

### 5. Measurable

Every optimization should eventually be evaluated against a baseline.

---

# 🏆 Alignment With the Challenge

UrjaIQ directly addresses the major areas identified in the challenge:

| Challenge Requirement | UrjaIQ |
|---|---|
| Real-time energy monitoring | ✅ MQTT + live dashboard |
| Equipment visibility | ✅ Machine telemetry |
| Predictive/maintenance intelligence | ✅ ML anomaly detection |
| Process optimization | ✅ Energy optimization engine |
| Specific energy consumption | ✅ SEC calculation |
| Production quality | ✅ Good/rejected units |
| Carbon accounting | ✅ CO₂e estimation |
| Software prototype | ✅ Full working simulation |
| Quantified baseline | ✅ Baseline + optimization scenario |
| SME-focused architecture | ✅ Low-cost software-first approach |
| AI assistance | ✅ Factory AI Copilot |

---

# 🧑‍💻 Development

Built as a full-stack industrial intelligence prototype using:

```text
Frontend
    Next.js + React + TypeScript + Tailwind

Backend
    Python + FastAPI + SQLAlchemy

Database
    PostgreSQL

IoT
    MQTT + Mosquitto

ML
    Scikit-learn + Isolation Forest

AI
    Gemini API

Infrastructure
    Docker + Docker Compose

Version Control
    Git + GitHub
```

---

# 📜 License

This project is developed as a prototype for educational, innovation and hackathon purposes.

Add your chosen license here, for example:

```text
MIT License
```

if you decide to release the repository under MIT.

---

# 👨‍💻 Team

**UrjaIQ**

Built for the **Smart Manufacturing — Industrial Energy & Process Efficiency** challenge.

---

# ⭐ Final Message

> **UrjaIQ turns factory data into factory intelligence.**

Instead of asking only:

> *"How much energy did the factory consume?"*

UrjaIQ helps answer:

> **"Where was the energy consumed, what happened to production quality, which machines need attention, what can potentially be optimized, and what is the environmental impact?"**
