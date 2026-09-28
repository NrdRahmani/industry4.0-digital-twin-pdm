import os
import pandas as pd
import numpy as np
import psycopg2
import json # <-- Added for formatting data nicely
import paho.mqtt.client as mqtt # <-- Added for MQTT telemetry
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from dotenv import load_dotenv

load_dotenv()
# 1. Database Connection Parameters
# Securely pull the parameters
DB_SETTINGS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def train_predictive_model():
    print("🔌 Extracting historical sensor data from PostgreSQL...")
    conn = psycopg2.connect(**DB_SETTINGS)
    query = "SELECT timestamp, vibration_mm_s, bearing_temp_c, is_anomaly FROM pump_telemetry ORDER BY timestamp ASC;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    failure_timestamp = df[df['is_anomaly'] == 1]['timestamp'].max()
    df['RUL_Minutes'] = (failure_timestamp - df['timestamp']).dt.total_seconds() / 60.0
    
    X = df[['vibration_mm_s', 'bearing_temp_c']]
    y = df['RUL_Minutes']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 2. RUN SIMULATED LIVE PLC VALUE INFERENCING
    live_plc_vibration = 4.2
    live_plc_temperature = 78.5
    live_data_input = pd.DataFrame([[live_plc_vibration, live_plc_temperature]], columns=['vibration_mm_s', 'bearing_temp_c'])
    predicted_rul = model.predict(live_data_input)[0]
    
    # 3. NEW: THE INDUSTRY 4.0 MQTT BROADCAST ENGINE
    print("\n📡 Connecting to Mosquitto MQTT Broker...")
    
    # Create the predictive data payload as a clean JSON string
    telemetry_payload = {
        "pump_id": 1,
        "live_vibration": live_plc_vibration,
        "live_temperature": live_plc_temperature,
        "predicted_rul_minutes": round(predicted_rul, 1),
        "status_alert": "CRITICAL ANOMALY" if predicted_rul < 60 else "HEALTHY"
    }
    
    # Initialize the MQTT networking client
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60) # Connects to your local Mosquitto broker
    
    # Publish the JSON message string to an industrial topic channel
    mqtt_client.publish("factory/pump1/predictive_alerts", json.dumps(telemetry_payload))
    print(f"✅ Telemetry Payload successfully broadcasted to MQTT topic 'factory/pump1/predictive_alerts'")
    print(json.dumps(telemetry_payload, indent=4))
    
    mqtt_client.disconnect()

if __name__ == "__main__":
    train_predictive_model()
