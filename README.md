# CasaWise — House Price Prediction Frontend + API

This update adds a responsive frontend to the Flask API. It uses the existing trained model file.

## Important
Copy your existing `house_price_model.joblib` into this project folder before running or deploying. It is not included in this ZIP because your model is on your Mac and was not uploaded here.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
If port 5000 is occupied:
```bash
PORT=5001 python app.py
```
Open `http://127.0.0.1:5000/` (or port 5001 if selected). `/health` checks the model and `/api` shows API information. The frontend sends POST requests to `/predict`.

## Deploy updated frontend
1. Copy these files/folders into your existing `house_price_prediction_api` project, replacing `app.py` and adding `templates/` and `static/`.
2. Ensure `house_price_model.joblib` remains in the project root.
3. Commit and push to the same GitHub repository that Render uses. Render should redeploy automatically.
4. Open your existing Render service URL to see the frontend.

## Model input schema
The API sends a DataFrame with `location`, `total_sqft`, `bedrooms`, and `bath`, matching the verified feature names from the saved model.
