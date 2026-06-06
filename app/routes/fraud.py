from app.services.logging_service import save_log
from fastapi import APIRouter
from pydantic import BaseModel
import joblib

router = APIRouter()

# Load model
model = joblib.load("app/models/fraud_model.pkl")


class Transaction(BaseModel):
    amount: float
    device_change: int
    location_change: int
    transactions_today: int


@router.post("/predict-fraud")
def predict_fraud(transaction: Transaction):

    data = [[
        transaction.amount,
        transaction.device_change,
        transaction.location_change,
        transaction.transactions_today
    ]]

    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0][1]

    risk_score = round(probability * 100, 2)

    save_log({
    "module": "fraud_detection",
    "input": {
        "amount": transaction.amount,
        "device_change": transaction.device_change,
        "location_change": transaction.location_change,
        "transactions_today": transaction.transactions_today
    },
    "output": {
        "fraud_risk": int(prediction),
        "risk_score": risk_score,
        "status": (
            "Suspicious"
            if prediction == 1
            else "Normal"
        )
    }
})

    return {
        "fraud_risk": int(prediction),
        "risk_score": risk_score,
        "status": "Suspicious" if prediction == 1 else "Normal"
    }



# Load failure analysis model
failure_model = joblib.load("app/models/failure_model.pkl")

# Load encoder
failure_encoder = joblib.load("app/models/failure_encoder.pkl")


class FailureTransaction(BaseModel):
    amount: float
    network_status: int
    balance: float
    retry_count: int


@router.post("/analyze-failure")
def analyze_failure(transaction: FailureTransaction):

    data = [[
        transaction.amount,
        transaction.network_status,
        transaction.balance,
        transaction.retry_count
    ]]

    prediction = failure_model.predict(data)[0]

    probabilities = failure_model.predict_proba(data)[0]

    confidence = round(max(probabilities) * 100, 2)

    reason = failure_encoder.inverse_transform([prediction])[0]

    return {
        "failure_reason": reason,
        "confidence": confidence
    }


# Load AML model
aml_model = joblib.load("app/models/aml_model.pkl")

# Load AML encoder
aml_encoder = joblib.load("app/models/aml_encoder.pkl")


class AMLTransaction(BaseModel):
    transaction_amount: float
    night_transaction: int
    multiple_transfers: int
    new_device: int
    international_transfer: int


@router.post("/aml-risk")
def aml_risk(transaction: AMLTransaction):

    data = [[
        transaction.transaction_amount,
        transaction.night_transaction,
        transaction.multiple_transfers,
        transaction.new_device,
        transaction.international_transfer
    ]]

    prediction = aml_model.predict(data)[0]

    probabilities = aml_model.predict_proba(data)[0]

    confidence = round(max(probabilities) * 100, 2)

    risk_level = aml_encoder.inverse_transform([prediction])[0]

    return {
        "aml_risk_score": confidence,
        "risk_level": risk_level
    }


# Load anomaly model
anomaly_model = joblib.load("app/models/anomaly_model.pkl")


class AnomalyTransaction(BaseModel):
    amount: float
    transaction_hour: int
    device_change: int
    location_change: int
    transactions_today: int


@router.post("/detect-anomaly")
def detect_anomaly(transaction: AnomalyTransaction):

    data = [[
        transaction.amount,
        transaction.transaction_hour,
        transaction.device_change,
        transaction.location_change,
        transaction.transactions_today
    ]]

    prediction = anomaly_model.predict(data)[0]

    anomaly_detected = bool(prediction == -1)

    anomaly_score = anomaly_model.decision_function(data)[0]

    normalized_score = min(99.0, float(
        round(abs(anomaly_score) * 1000, 2))
    )

    return {
        "anomaly_detected": anomaly_detected,
        "anomaly_score": normalized_score,
        "message": (
            "Unusual transaction behavior detected"
            if anomaly_detected
            else "Transaction behavior appears normal"
        )
    }