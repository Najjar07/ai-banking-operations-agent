import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("datasets/fraud_data.csv")

# Features
X = df[[
    "amount",
    "device_change",
    "location_change",
    "transactions_today"
]]

# Target
y = df["fraud"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy}")

# Save model
joblib.dump(model, "app/models/fraud_model.pkl")

print("Fraud model saved successfully")