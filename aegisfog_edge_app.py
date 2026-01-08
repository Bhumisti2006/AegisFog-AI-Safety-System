from azure.iot.device import IoTHubDeviceClient, Message
import joblib
import pandas as pd
import time
from collections import deque
import warnings

warnings.filterwarnings("ignore")

# ----------------------------
# AZURE IOT HUB CLIENT
# ----------------------------
import os

CONNECTION_STRING = os.getenv("IOT_CONNECTION_STRING")

iot_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

print("✅ Edge app started...")

# ----------------------------
# LOAD MODEL (AZURE ML OUTPUT)
# ----------------------------
model = joblib.load("aegisfog_risk_model.pkl")
print("✅ Model loaded")

# ----------------------------
# VEHICLE PROFILE
# ----------------------------
profile = {
    "friction": 0.6,
    "ttc_threshold": 3.0
}

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def braking_unavoidable(speed_mps, distance_m, friction):
    g = 9.81
    stopping_distance = (speed_mps ** 2) / (2 * friction * g)
    return distance_m < stopping_distance

def compute_ttc(distance, speed):
    speed = abs(speed)
    return distance / speed if speed > 0 else 1000

# ----------------------------
# STATE VARIABLES (IMPORTANT)
# ----------------------------
braking_applied = False
alert_active = False
danger_sent = False
clear_sent = False

# ----------------------------
# SIMULATION SETUP
# ----------------------------
distance = 60
relative_speed = -12
fog_density = 0.7
time_step = 1

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    # Update environment
    distance += relative_speed * time_step

    # Compute TTC
    ttc = compute_ttc(distance, relative_speed)

    # AI Prediction (Edge ML)
    features = pd.DataFrame([{
        "distance": distance,
        "relative_speed": relative_speed,
        "fog_density": fog_density,
        "ttc": ttc
    }])
    risk = model.predict(features)[0]

    # Physics safety
    physics_block = braking_unavoidable(
        abs(relative_speed),
        distance,
        profile["friction"]
    )

    # Alert condition
    alert = (ttc < profile["ttc_threshold"]) or physics_block

    # ----------------------------
    # EDGE BEHAVIOR (REAL TIME)
    # ----------------------------
    if alert:
        alert_active = True
        braking_applied = True
        print(f"🚨 RED ALERT: BRAKE NOW | distance={distance:.1f}m | TTC={ttc:.2f}s")

        # SEND ONLY ONCE TO IOT HUB
        if not danger_sent:
            telemetry = {
                "deviceId": "aegisfog-virtual-sensor",
                "event": "DANGER_ALERT",
                "distance": float(distance),
                "ttc": float(ttc),
                "fog_density": float(fog_density)
            }
            iot_client.send_message(Message(str(telemetry)))
            print("📡 DANGER alert sent to Azure IoT Hub")
            danger_sent = True

    else:
        if alert_active:
            print("🟢 SAFE DISTANCE RESTORED")

            # SEND CLEAR EVENT ONLY ONCE
            if not clear_sent:
                telemetry = {
                    "deviceId": "aegisfog-virtual-sensor",
                    "event": "ALERT_CLEARED",
                    "distance": float(distance),
                    "ttc": float(ttc)
                }
                iot_client.send_message(Message(str(telemetry)))
                print("📡 CLEAR alert sent to Azure IoT Hub")
                clear_sent = True

        alert_active = False
        print(f"🟢 Monitoring... | distance={distance:.1f}m | TTC={ttc:.2f}s")

    # ----------------------------
    # BRAKING SIMULATION
    # ----------------------------
    if braking_applied:
        relative_speed += 4
        if relative_speed >= 0:
            print("🛑 Vehicle stopped safely")
            break

    # ----------------------------
    # COLLISION CHECK (LAST)
    # ----------------------------
    if distance <= 0:
        print("💥 Collision occurred")
        break

    time.sleep(1)
