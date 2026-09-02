import os
import joblib
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

MODEL_PATH = 'model/model.pkl'


def train_and_save_model():
  """Train linear regression model and save it to disk."""
  os.makedirs('model', exist_ok=True)
  X, y = make_regression(
      n_samples=100, n_features=2, noise=0.1, random_state=42
  )

  model = LinearRegression()
  model.fit(X, y)

  joblib.dump(model, MODEL_PATH)
  return model


def load_or_train_model():
  """Reuse existing trained model if available; otherwise train a new model."""
  if os.path.exists(MODEL_PATH):
    return joblib.load(MODEL_PATH)
  return train_and_save_model()


def predict_features(features):
  """Make prediction using the loaded model."""
  model = load_or_train_model()
  return float(model.predict([features])[0])