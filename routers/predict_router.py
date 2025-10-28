# routers/predict_router.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services import prediction_service

router = APIRouter()

@router.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """Predict the disease from an uploaded plant image"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        contents = await file.read()
        result = prediction_service.get_prediction(contents)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.get("/")
async def root():
    return {"message": "Plant Disease Detection API", "endpoint": "/predict"}