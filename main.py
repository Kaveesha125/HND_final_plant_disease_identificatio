from fastapi import FastAPI
from routers import predict_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Plant Disease Detection API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router.router)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8001)