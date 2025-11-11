# Plant Disease Detection 

> [!NOTE]
> 🌿 This is a **sub-microservice** of the main website for the **HND Final Project**.

A lightweight FastAPI service for identifying plant diseases from an uploaded image. It uses a quantized TensorFlow Lite model (`model.tfliteQuant`) for fast and efficient local inference.

## Quick Start

1.  **Create virtual environment & install dependencies**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2.  **Configure environment variables**
    ```
    SUPABASE_URL=your-supabase-url
    SUPABASE_KEY=your-supabase-key
    ```
> [!IMPORTANT]
> **You must add these to a `.env` file.**
> (Note: These are for the included Supabase client, though auth is not currently applied to endpoints).

3.  **Run the server**
    ```bash
    # Runs on http://localhost:8001
    uvicorn main:app --reload
    ```
## API Endpoints

> Base URL: `http://localhost:8001`

> [!TIP]
> This service includes interactive API documentation (Swagger UI). Once the server is running, you can test all endpoints at: **`http://localhost:8001/docs`**

* **GET `/`**
    * Root endpoint, returns a welcome message. (No input needed).

* **POST `/predict`**
    * Analyzes an uploaded image and returns the predicted plant disease and confidence score.
    * **Example Input (in Swagger UI):**
        * `file`: (Use the "Choose File" button to upload an image like `tomato_leaf.jpg`)
    * **Example Response:**
        ```json
        {
          "disease": "Tomato_Late_blight",
          "confidence": "98.45%",
          "all_predictions": {
            "Tomato_Late_blight": "98.45%",
            "Tomato_Early_blight": "1.05%",
            "Tomato_healthy": "0.50%"
          }
        }
        ```
