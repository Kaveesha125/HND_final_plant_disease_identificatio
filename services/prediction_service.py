# services/prediction_service.py
import tensorflow as tf
from PIL import Image
import numpy as np
import io

MODEL_PATH = "model.tfliteQuant"
LABELS_PATH = "Labels.txt"

# Load the TensorFlow Lite model
try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]['shape']
    height, width = input_shape[1], input_shape[2]
except Exception as e:
    raise RuntimeError(f"Failed to load model or model details: {e}")


# Load class labels
try:
    with open(LABELS_PATH, "r") as f:
        CLASS_NAMES = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    raise RuntimeError(f"Labels file not found at {LABELS_PATH}")

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Resize and normalize image for model prediction"""
    image = image.resize((width, height))
    image_array = np.array(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def get_prediction(image_bytes: bytes) -> dict:
    """Run inference on the provided image bytes."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    processed_image = preprocess_image(image)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], processed_image)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]

    predicted_class_idx = int(np.argmax(predictions))
    confidence = float(predictions[predicted_class_idx])
    disease_name = CLASS_NAMES[predicted_class_idx]

    return {
        "disease": disease_name,
        "confidence": f"{confidence * 100:.2f}%",
        "all_predictions": {
            CLASS_NAMES[i]: f"{predictions[i] * 100:.2f}%"
            for i in range(len(CLASS_NAMES))
        }
    }