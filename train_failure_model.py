import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("datasets/transaction_logs.csv")

# Encode target labels
encoder = LabelEncoder()

df["failure_reason_encoded"] = encoder.fit_transform(
    df["failure_reason"]
)

# Features
X = df[[
    "amount",
    "network_status",
    "balance",
    "retry_count"
]]

# Target
y = df["failure_reason_encoded"]

# Split dataset
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
joblib.dump(model, "app/models/failure_model.pkl")

# Save encoder
joblib.dump(encoder, "app/models/failure_encoder.pkl")

print("Failure analysis model saved successfully")