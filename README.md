# AegisFog-AI-Safety-System
AegisFog delivers real‑time collision prevention at the edge while using Azure for intelligent model training and efficient cloud monitoring.
# AegisFog – Edge‑First AI Safety System for Foggy Conditions

AegisFog is an **edge‑first AI safety system** designed to prevent collisions in low‑visibility (foggy) conditions.  
It combines **Azure Machine Learning**, **Edge AI**, and **Azure IoT Hub** to deliver **real‑time safety alerts** with **cloud‑efficient telemetry**.

---

## 🚀 Problem Statement
In foggy conditions, drivers often fail to perceive obstacles in time, leading to delayed braking and collisions.  
Cloud‑only systems suffer from latency and connectivity issues, making them unreliable for safety‑critical decisions.

---

## 💡 Our Solution
AegisFog performs **real‑time risk assessment at the edge**, ensuring immediate alerts, while **Azure handles training, monitoring, and scalability**.

### Key Design Principle
> **Safety decisions at the edge, visibility in the cloud.**

---

## 🧠 System Architecture

Azure Machine Learning
└── Model training & validation
↓
Edge AI (Python Application)
├── TTC calculation
├── Physics-based braking check
├── ML inference (.pkl model)
└── Persistent RED ALERT to driver
↓
Azure IoT Hub
├── DANGER_ALERT event
└── ALERT_CLEARED event


---

## 🔧 Technologies Used

- **Azure Machine Learning** – Model training and experimentation  
- **Azure IoT Hub** – Secure telemetry ingestion and monitoring  
- **Azure CLI** – Live event monitoring (`az iot hub monitor-events`)  
- **Python** – Edge application  
- **Scikit‑learn / Joblib** – Model serialization  
- **Pandas** – Feature handling  

---

## ⚙️ How the System Works

### 1️⃣ Edge AI (Real‑Time)
- Continuously monitors:
  - Distance
  - Relative speed
  - Fog density
  - Time‑to‑Collision (TTC)
- Triggers a **persistent RED ALERT** until a safe state is restored.

### 2️⃣ Cloud Telemetry (Azure IoT Hub)
- Sends **only state‑change events**:
  - `DANGER_ALERT` → when unsafe condition begins
  - `ALERT_CLEARED` → when safety is restored
- Prevents cloud message flooding and reduces cost.

---

## 📡 Azure IoT Hub Event Flow

| Event | Trigger Condition |
|-----|------------------|
| `DANGER_ALERT` | TTC below threshold or braking unavoidable |
| `ALERT_CLEARED` | Safe distance / TTC restored |

Verified using:
```bash
az iot hub monitor-events --hub-name aegisfog-iot-hub
Observed Events:
DANGER_ALERT when TTC falls below threshold

ALERT_CLEARED when vehicle reaches safe distance

This confirms live Edge → Azure integration.

Key Features
⚡ Ultra‑low latency edge decision making

🌐 Cloud‑agnostic safety (works even without internet)

☁️ Azure‑backed intelligence & monitoring

🔁 State‑based alerting (industry‑grade design)

📉 Minimal cloud message overhead

🧪 Validation & Results
Edge console confirms:

Persistent RED ALERT during danger

Safe stop without collision

Azure IoT Hub confirms:

Exactly one DANGER event

Exactly one CLEAR event

This mirrors real automotive safety systems.

📁 Project Structure
├── aegisfog_edge_app.py
├── aegisfog_risk_model.pkl
├── README.md
