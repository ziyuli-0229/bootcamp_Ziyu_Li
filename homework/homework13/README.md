# Stage 13 Homework - Prediction API

This API serves real-time predictions from a trained scikit-learn Linear Regression model using synthetic two-feature data. It provides lightweight HTTP endpoints supporting both JSON payloads and URL path parameters.

## Running the Server

Run the following command to start the Flask service:

    python app.py

The server runs on http://127.0.0.1:5000 and automatically loads `model/model.pkl` at startup.

## POST /predict

Send a JSON payload containing a 2-feature array:

    curl -X POST http://127.0.0.1:5000/predict \
         -H "Content-Type: application/json" \
         -d "{\"features\": [0.1, 0.2]}"

Response:
```json
{"prediction": 23.58961171297328}