from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Define a model for storing predictions
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, nullable=False)  # Change this to db.Integer
    prediction = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database and the table
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database: {e}")

# Load the trained model
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    input_data = data['input']
    prediction = model.predict(np.array(input_data).reshape(1, -1))
    prediction_result = int(prediction[0])

    # Store the prediction in the database
    new_prediction = Prediction(input_data=str(input_data), prediction=str(prediction_result))
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({'prediction': prediction_result})

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    data = request.get_json(force=True)
    inputs = data['inputs']
    predictions = model.predict(np.array(inputs))
    predictions_list = predictions.tolist()

    # Store each prediction in the database
    for input_data, prediction in zip(inputs, predictions_list):
        new_prediction = Prediction(input_data=str(input_data), prediction=str(prediction))
        db.session.add(new_prediction)
    db.session.commit()

    return jsonify({'predictions': predictions_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
