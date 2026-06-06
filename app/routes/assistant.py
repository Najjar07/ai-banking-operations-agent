from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AssistantRequest(BaseModel):
    fraud_risk: int
    aml_risk_score: float
    anomaly_detected: bool
    failure_reason: str


@router.post("/banking-assistant")
def banking_assistant(request: AssistantRequest):

    responses = []

    # Fraud explanation
    if request.fraud_risk == 1:
        responses.append(
            "Transaction appears suspicious due to unusual behavior patterns."
        )

    # AML explanation
    if request.aml_risk_score > 70:
        responses.append(
            "High AML risk detected because of suspicious transaction activity."
        )

    # Anomaly explanation
    if request.anomaly_detected:
        responses.append(
            "Anomalous transaction behavior detected from transaction patterns."
        )

    # Failure explanation
    if request.failure_reason != "success":
        responses.append(
            f"Transaction failure likely caused by {request.failure_reason}."
        )

    # Default response
    if not responses:
        responses.append(
            "Transaction appears normal with no major operational risk detected."
        )

    return {
        "assistant_analysis": responses
    }