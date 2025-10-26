from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
from PIL import Image
import numpy as np
import io

app = FastAPI(title="Plant Disease Detection API")

MODEL_PATH = "model.tfliteQuant"
LABELS_PATH = "Labels.txt"

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Get model input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Detect model input shape dynamically
input_shape = input_details[0]['shape']
height, width = input_shape[1], input_shape[2]

# Load class labels
with open(LABELS_PATH, "r") as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Resize and normalize image for model prediction"""
    image = image.resize((width, height))
    image_array = np.array(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """Predict the disease from an uploaded plant image"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        processed_image = preprocess_image(image)

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], processed_image)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]

        predicted_class_idx = int(np.argmax(predictions))
        confidence = float(predictions[predicted_class_idx])
        disease_name = CLASS_NAMES[predicted_class_idx]

        return JSONResponse(content={
            "disease": disease_name,
            "confidence": f"{confidence * 100:.2f}%",
            "all_predictions": {
                CLASS_NAMES[i]: f"{predictions[i] * 100:.2f}%"
                for i in range(len(CLASS_NAMES))
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Plant Disease Detection API", "endpoint": "/predict"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
