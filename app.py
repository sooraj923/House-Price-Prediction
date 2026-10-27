from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.environ.get("MODEL_PATH", BASE_DIR / "house_price_model.joblib"))

try:
    model = joblib.load(MODEL_PATH)
    print("House price prediction model loaded successfully.")
except Exception as exc:
    model = None
    print(f"Model loading failed: {exc}")


@app.route("/", methods=["GET"])
def home():
    # Render the frontend in browsers; the API is still available at /predict.
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    if model is None:
        return jsonify({"status": "unhealthy", "model_loaded": False}), 503
    return jsonify({"status": "healthy", "model_loaded": True}), 200


@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({
        "message": "Bengaluru House Price Prediction API",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "health": "/health",
            "predict": "POST /predict"
        }
    })


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model is not loaded. Check the model file."}), 503

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Please send valid JSON data."}), 400

    required_fields = ["location", "total_sqft", "bedrooms", "bath"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    try:
        location = str(data["location"]).strip()
        total_sqft = float(data["total_sqft"])
        bedrooms = int(data["bedrooms"])
        bath = float(data["bath"])

        if not location:
            raise ValueError("Please enter a location.")
        if total_sqft <= 0 or bedrooms <= 0 or bath <= 0:
            raise ValueError("Area, bedrooms, and bathrooms must be greater than zero.")
    except (ValueError, TypeError, OverflowError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400

    house = pd.DataFrame([{
        "location": location.lower(),
        "total_sqft": total_sqft,
        "bedrooms": bedrooms,
        "bath": bath
    }])

    try:
        prediction = float(model.predict(house)[0])
        return jsonify({
            "predicted_price_lakhs": round(prediction, 2),
            "currency": "INR",
            "unit": "lakhs",
            "input": {
                "location": location,
                "total_sqft": total_sqft,
                "bedrooms": bedrooms,
                "bath": bath
            }
        }), 200
    except Exception as exc:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed. Check the model's expected inputs.",
            "details": str(exc)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
