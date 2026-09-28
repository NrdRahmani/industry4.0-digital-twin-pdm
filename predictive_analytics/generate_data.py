import os
import datetime
import random
import numpy as np
import pandas as pd
import psycopg2
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


def create_and_populate_db():
    print("⏳ Connecting to PostgreSQL...")
    conn = psycopg2.connect(**DB_SETTINGS)
    cursor = conn.cursor()

    # Create the table schema
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pump_telemetry (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            pump_id INT NOT NULL,
            vibration_mm_s REAL NOT NULL,
            bearing_temp_c REAL NOT NULL,
            is_anomaly INT DEFAULT 0
        );
    """
    )
    conn.commit()
    print("✅ Table 'pump_telemetry' verified/created.")

    # 2. Simulate 10 days of sensor data (sampled every 5 minutes)
    print("📊 Generating 10 days of simulated operational data...")
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    records = []

    # Total timestamps: 10 days * 24 hours * 12 intervals/hr = 2880 rows
    total_intervals = 10 * 24 * 12

    # Initial baseline values (Healthy machine)
    base_temp = 42.0
    base_vib = 1.8

    for i in range(total_intervals):
        current_time = start_time + datetime.timedelta(minutes=5 * i)

        # Introduce a slow, artificial degradation over the final 2 days
        progress_ratio = i / total_intervals
        if progress_ratio > 0.8:  # Final 20% of the dataset represents failure path
            degradation_factor = (progress_ratio - 0.8) * 5.0
            anomaly_flag = 1
        else:
            degradation_factor = 0.0
            anomaly_flag = 0

        # Add random sensor noise
        temp = base_temp + (degradation_factor * 8.0) + random.uniform(-1.2, 1.2)
        vib = base_vib + (degradation_factor * 1.5) + random.uniform(-0.3, 0.3)

        records.append((current_time, 1, float(vib), float(temp), anomaly_flag))

    # 3. Bulk insert rows into PostgreSQL
    print("💾 Inserting records into database...")
    insert_query = """
        INSERT INTO pump_telemetry (timestamp, pump_id, vibration_mm_s, bearing_temp_c, is_anomaly)
        VALUES (%s, %s, %s, %s, %s);
    """
    cursor.executemany(insert_query, records)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"🎉 Success! {len(records)} entries successfully written to PostgreSQL.")


if __name__ == "__main__":
    create_and_populate_db()
