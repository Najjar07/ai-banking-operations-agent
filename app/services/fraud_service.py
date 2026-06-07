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

    risk_score = float(model.predict_proba(data)[0][1] * 100)

    if prediction == 1:
        status = "Suspicious"
    else:
        status = "Normal"

    return {
        "fraud_risk": int(prediction),
        "risk_score": round(risk_score, 2),
        "status": status
    }