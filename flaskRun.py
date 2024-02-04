# from pandas import json_normalize
from terra.base_client import Terra
import logging
import flask
from flask import request
import requests
from flask_cors import CORS


import time
from json_norm import normalize_json
import json
# import joblib
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow import keras
import numpy as np

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

API_KEY = "O8sTDuQBXJfQDlULKMZrnOKlzzRNHMpi"
DEV_ID = "ichack-testing-cgyBGcj290"
SECRET = "4edcc0dfbabb6a58094bcdf64c51595d7161773fcd6a267b"


terra = Terra(API_KEY, DEV_ID, SECRET)

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("app")

app = flask.Flask(__name__)

CORS(app)


@app.route("/")
def home():

    #Mock loading json -> will be getting body

    # protoper = "protoper.json"
    # with open(protoper, 'r') as file:
    #     protoper_data = json.load(file)
    # protoper = normalize_json(protoper_data)

    #Loading model (LR)
    '''
    loaded_model = joblib.load('model.joblib')
    protoper_scaled = protoper.drop(['active_seconds'], axis=1)
    predicted_active_seconds = loaded_model.predict(protoper_scaled)
    print("Predicted Active minutes:")
    print(predicted_active_seconds / 60)
    '''
    #Loading nicer model (NN)
    # loaded_model = keras.models.load_model('test_train.keras')
    # np_data = protoper.to_numpy()
    # new_data_expanded = np.expand_dims(np_data, axis=1)
    # predictions = loaded_model.predict(new_data_expanded,verbose=0)
    # print(f'Predicted Active minutes: {predictions/60}')

    return "hello world"


@app.route("/consumeTerraWebhook", methods=["POST"])
def consume_terra_webhook() -> flask.Response:
    body_str = str(request.get_data(), 'utf-8')
    body = request.get_json()

    print(request.headers)
    # ML to be inserted
    _LOGGER.info(
        "Received webhook for user %s of type %s",
        body.get("user", {}).get("user_id"),
        body["type"])
    verified = terra.check_terra_signature(request.get_data().decode("utf-8"), request.headers['terra-signature'])
    if verified:
        return flask.Response(status=200)
    else:
        return flask.Response(status=403)


base_url = "https://6b0c-2a0c-5bc0-40-3e3d-13ec-d32e-b440-2277.ngrok-free.app/"


@app.route("/connect")
def connect():
    response = requests.post("https://api.tryterra.co/v2/auth/generateWidgetSession", headers={ \
        "dev-id": DEV_ID, "x-api-key": API_KEY \
        }, json={"reference_id": "test-username1", "lang": "en",
                 'auth_success_redirect_url': f'{base_url}/on_auth_success'})
    url = response.json()["url"]
    print(url, response.json())
    return url


@app.route("/send", methods=['POST'])
def send():
    user_id = request.args.get("user_id")
    start_data = "2024-02-04"
    start_data = "2024-02-04"
    url = "https://api.tryterra.co/v2/sleep?user_id="+user_id+"&start_date="+start_data+"&end_date="+end_data+"&to_webhook=true&with_samples=true"
    headers = {
        "accept": "application/json",
        "dev-id": DEV_ID,
        "x-api-key": API_KEY
    }



    response = requests.get(url, headers=headers)
    returnedData = response.json()
    loaded_model = keras.models.load_model('test_train.keras')
    np_data = returnedData.to_numpy()
    new_data_expanded = np.expand_dims(np_data, axis=1)
    predictions = loaded_model.predict(new_data_expanded,verbose=0)
    print(f'Predicted Active minutes: {predictions/60}')

    

    return f'Predicted Active minutes: {predictions/60}'

@app.route("/on_auth_success", methods=['GET'])
def on_auth_success():
    user_id = request.args.get('user_id')
    print(user_id)
    # time.sleep(3)
    # send SSE
    return user_id
    

if __name__ == "__main__":
    app.run(host="localhost", port=8080)
