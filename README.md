# Industrial Digital Twin & Predictive Maintenance (PdM) End-to-End Sandbox

An enterprise-grade Industry 4.0 architecture featuring a 3D Digital Twin, text-based PLC control, a high-performance relational database historian, and a Python-driven Machine Learning predictive analytics engine.

## 🌐 System Architecture & Data Flow

```text
 [🏭 Factory I/O] ======= (Profinet) =======> [🧠 Siemens TIA Portal / PLCSIM]
 (3D Digital Twin)                                     ||
                                                 (NetToPLCSim)
                                                       ||
 [🗄️ PostgreSQL]  <==== (SQL Engine) ====>  [📊 Ignition SCADA] <===> [🐍 Python / VS Code]
 (Data Historian)                             (Central Control)       (Custom Integration)
                                                       ||
 [🟢 Node-RED]   <====== (MQTT) ======>  [🦟 Mosquitto Broker] <===> [🔍 MQTT Explorer]
(Data Routing)                              (IIoT Messaging)         (Traffic Monitor)
```

## 🛠️ Tech Stack & Industrial Tooling

- **Industrial Automation (OT):** Siemens TIA Portal (STEP 7, WinCC), Siemens SCL (Structured Control Language), PLCSIM, Factory I/O (3D Visual Twin Platform).
- **SCADA & Application Scripting:** Ignition SCADA (Standard / Perspective Core), Jython / Python Core Automation.
- **Data Engineering & Historian:** PostgreSQL, pgAdmin 4, Relational Time-Series Database Schema Design.
- **Industrial IoT (IIoT) Protocols:** MQTT (Mosquitto Broker), MQTT Explorer, OPC UA Server/Client Topologies, Node-RED Event-Driven Workflows.
- **Data Science:** Python 3, Pandas, NumPy, Scikit-Learn (Random Forest Regressor, Isolation Forest).

## 🚀 Key Architectural Milestones Developed

1. **Text-Based PLC Logic Design:** Bypassed traditional rigid ladder constraints by engineering modular factory sequence algorithms using **Siemens SCL (Structured Text)**.
2. **3D Digital Twin Commissioning:** Synchronized real-time physical telemetry using **Factory I/O** mapped directly to an emulated S7-1200 CPU, validating automation logic virtually.
3. **Enterprise SCADA Integration:** Configured an **Ignition Standard** gateway backend to bind industrial OPC UA tags with web-responsive visual dashboards.
4. **Machine Learning Predictive Core (PdM):** Processed continuous high-frequency bearing data inside **PostgreSQL** to train a Scikit-Learn **Random Forest Regressor**, calculating **Remaining Useful Life (RUL)** metrics down to the minute.
5. **Event-Driven IIoT Pipeline:** Built an over-the-air microservices broker loop using **MQTT** and **Node-RED** to instantly broadcast critical mechanical anomaly alerts across the local network interface.

## 🔒 Security Best Practices
All sensitive environment variables, database strings, and master root passwords have been fully abstracted out of the code files and stored locally inside a secured `.env` container, managed via a `.gitignore` baseline to prevent unauthorized credential leaks.
