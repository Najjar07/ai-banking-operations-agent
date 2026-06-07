import joblib
import pandas as pd

model = joblib.load("app/models/fraud_model.pkl")

def predict_fraud(amount, device_change, location_change, transactions_today):

    data = pd.DataFrame([{
        "amount": amount,
        "device_change": device_change,
        "location_change": location_change,
        "transactions_today": transactions_today
    }])

    prediction = model.predict(data)[0]

    return {
        "fraud_risk": int(prediction),
        "status": "Suspicious" if prediction == 1 else "Safe"
    }