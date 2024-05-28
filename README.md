
---

# Titanic Survival Prediction API

This repository contains a Flask web application that predicts the survival of a Titanic passenger based on specific input features. The prediction model is based on a Logistic Regression model from [Kaggle's Titanic Data Science Solutions](https://www.kaggle.com/code/startupsci/titanic-data-science-solutions).

## Features

The prediction is based on the following input features  [Pclass,Sex,Age,Embarked,Title,IsAlone,AgeClass]: 
- **Pclass**: Passenger class (integer from 1 to 3)
- **Sex**: Gender (male=0, female=1)
- **Age**: Age of the passenger
- **Embarked**: Port of Embarkation (integer from 0 to 3)
- **Title**: Title of the passenger ("Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5)
- **IsAlone**: Whether the passenger is alone (True=1, False=0)
- **AgeClass**: Age multiplied by Pclass, where Age is bucketed as:
  - 0 if age <= 16
  - 1 if 16 < age <= 32
  - 2 if 32 < age <= 48
  - 3 if 48 < age <= 64
  - 4 if age > 64

## Usage

To get a survival prediction, provide the above parameters as input, and the API will return a survival prediction (either 0 or 1).

## Data

The data for training (`xtrain.csv`, `ytrain.csv`) is also taken from the aforementioned Kaggle source.

## Files

- **code_titan_test.py**: Contains the code for creating the Logistic Regression model and saving it as `model.pkl`.
- **app.py**: Sets up a Flask web application that provides an API for making predictions using the pre-trained machine learning model.

## Docker Setup

### Dockerfile

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      FLASK_ENV: development
    command: flask run --host=0.0.0.0
```

### requirements.txt

```
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
joblib==1.1.0
numpy==1.21.2
pandas==1.3.3
scikit-learn==1.0
```

## API Endpoints

### `/predict`
Accepts POST requests with input data and returns a survival prediction. Stores the input data and prediction result in the database.

### `/predict_batch`
Accepts POST requests with a batch of input data and returns a list of survival predictions. Stores each input data and prediction result in the database.

## Setup Instructions

### Local Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Create and train the model**:
    ```sh
    python code_titan_test.py
    ```

4. **Run the Flask app**:
    ```sh
    python app.py
    ```

5. **Access the API**:
    The API will be available at `http://0.0.0.0:5000`.

### Docker Setup

1. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

2. **Access the API**:
    The API will be available at `http://0.0.0.0:5000`.

## Test the API


**Single prediction using curl**:
```sh
curl -X POST http://localhost:5000/predict_batch -H "Content-Type: application/json" -d '{"inputs": [[3, 0, 0, 0,0,0,0,0],[3, 0, 0, 0,0,0,0,0]]}'
```

**batch prediction using curl**:
```sh
curl -X POST http://localhost:5000/predict_batch -H "Content-Type: application/json" -d '{"inputs": [[3, 0, 0, 0,0,0,0,0],[3, 0, 0, 0,0,0,0,0]]}'
 ```


## Detailed Code Description

### app.py
This code sets up a Flask web application that provides an API for making predictions using a pre-trained machine learning model.

1. **Initialize Flask App**: Initializes a Flask web application.
2. **Configure Database**: Configures an SQLite database using SQLAlchemy to store prediction results.
3. **Define Database Model**: Defines a `Prediction` model to store input data, prediction result, and timestamp for each prediction made.
4. **Create Database**: Creates the database and the table if they do not already exist.
5. **Load Pre-trained Model**: Loads a pre-trained machine learning model from `model.pkl`.
6. **Define Prediction Endpoint**: The `/predict` endpoint accepts POST requests with input data, makes a prediction using the pre-trained model, stores the prediction in the database, and returns the prediction result.
7. **Define Batch Prediction Endpoint**: The `/predict_batch` endpoint accepts POST requests with a batch of input data, makes predictions for each input using the pre-trained model, stores each prediction in the database, and returns the list of predictions.
8. **Run the App**: Configures the Flask app to run on host `0.0.0.0` and port `5000`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

