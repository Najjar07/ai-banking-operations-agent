import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load dataset
df = pd.read_csv("datasets/anomaly_data.csv")

# Features
X = df[[
    "amount",
    "transaction_hour",
    "device_change",
    "location_change",
    "transactions_today"
]]

# Train anomaly model
model = IsolationForest(
    contamination=0.3,
    random_state=42
)

model.fit(X)

# Save model
joblib.dump(model, "app/models/anomaly_model.pkl")

print("Anomaly detection model saved successfully")