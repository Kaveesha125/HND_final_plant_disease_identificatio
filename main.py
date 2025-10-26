# main.py
from fastapi import FastAPI
from routers import predict_router
import uvicorn

app = FastAPI(title="Plant Disease Detection API")

app.include_router(predict_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
