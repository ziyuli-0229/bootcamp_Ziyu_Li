import os
from flask import Flask, jsonify, request
import joblib

app = Flask(__name__)

MODEL_PATH = 'model/model.pkl'

# Load saved model once at startup or train if missing
if os.path.exists(MODEL_PATH):
  model = joblib.load(MODEL_PATH)
else:
  from src.pipeline import train_and_save_model

  model = train_and_save_model()


# POST endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict_post():
  data = request.get_json(silent=True) or {}
  features = data.get('features')

  if (
      not isinstance(features, list)
      or len(features) != 2
      or not all(isinstance(x, (int, float)) for x in features)
  ):
    return (
        jsonify({
            'error': (
                'Invalid payload. "features" must be a list of 2 numbers.'
            )
        }),
        400,
    )

  prediction = float(model.predict([features])[0])
  return jsonify({'prediction': prediction})


# GET endpoint for prediction via path parameters
@app.route('/predict/<f1>/<f2>', methods=['GET'])
def predict_get(f1, f2):
  try:
    f1_val = float(f1)
    f2_val = float(f2)
  except (ValueError, TypeError):
    return (
        jsonify({'error': 'Path parameters f1 and f2 must be valid numbers.'}),
        400,
    )

  prediction = float(model.predict([[f1_val, f2_val]])[0])
  return jsonify({'prediction': prediction})


# Additional route: Trigger full analysis execution
@app.route('/run_full_analysis', methods=['GET'])
def run_full_analysis():
  from src.pipeline import train_and_save_model

  train_and_save_model()
  return jsonify({
      'status': 'success',
      'message': 'Full analysis re-run completed and model updated.',
  })


if __name__ == '__main__':
  app.run(port=5000)