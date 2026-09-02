from flask import Flask, request, jsonify
import joblib

# Load model ONCE at app startup (Do NOT load inside route functions)
model = joblib.load('model/model.pkl')
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict_post():
    data = request.get_json(silent=True) or {}
    features = data.get('features')

    # Validate that features exist and contain exactly 2 numbers
    if not isinstance(features, list) or len(features) != 2 or not all(isinstance(x, (int, float)) for x in features):
        return jsonify({'error': 'Invalid input. "features" must be a list of 2 numbers.'}), 400

    try:
        # Predict expects a 2D list: [[f1, f2]]
        prediction = float(model.predict([features])[0])
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/predict/<f1>/<f2>', methods=['GET'])
def predict_get(f1, f2):
    # Convert path parameters from string to float
    try:
        f1_val = float(f1)
        f2_val = float(f2)
    except (ValueError, TypeError):
        return jsonify({'error': 'Path parameters f1 and f2 must be valid numbers.'}), 400

    try:
        prediction = float(model.predict([[f1_val, f2_val]])[0])
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5000)
