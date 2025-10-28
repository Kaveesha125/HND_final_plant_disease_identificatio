# FILE: HND_final_disease_detection/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system-level dependencies (if any)
# (TensorFlow Lite often needs some .so files, but we'll try without first)

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all service code, including the model and labels file
COPY . .

EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]