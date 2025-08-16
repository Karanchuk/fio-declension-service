from fastapi import FastAPI
from app.models import DeclensionRequest, DeclensionResponse
from app.utils import decline_fio

app = FastAPI(title="FIO Declension Service", version="1.0")

@app.post("/decline", response_model=DeclensionResponse)
def decline(request: DeclensionRequest):
    declined = decline_fio(request.fio, request.case)
    return DeclensionResponse(original=request.fio, case=request.case, declined=declined)
