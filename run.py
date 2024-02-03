from terra.base_client import Terra
import logging
import flask
from flask import request
import requests

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer




API_KEY = "O8sTDuQBXJfQDlULKMZrnOKlzzRNHMpi"
DEV_ID = "ichack-testing-cgyBGcj290"
SECRET = "4edcc0dfbabb6a58094bcdf64c51595d7161773fcd6a267b"


terra = Terra(API_KEY, DEV_ID, SECRET)

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("app")


app = flask.Flask(__name__)

@app.route("/")
def home():
   return "hello world"

@app.route("/consumeTerraWebhook", methods=["POST"])
def consume_terra_webhook() -> flask.Response:
    # body_str = str(request.get_data(), 'utf-8')
    body = request.get_json()
    
    print(body)
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
@app.route("/connect" )
def connect():
    response = requests.post("https://api.tryterra.co/v2/auth/generateWidgetSession", headers={ \
    "dev-id": DEV_ID, "x-api-key": API_KEY \
    }, json={ "reference_id": "test-username", "lang": "en", 'auth_success_redirect_url': f'{base_url}/on_auth_success' })
    url = response.json()["url"]
    print(url, response.json())
    return flask.redirect(url,code=302)

@app.route("/on_auth_success", methods=['GET'])
def on_auth_success():
   
   return "hello world"
    
if __name__ == "__main__":
    app.run(host="localhost", port=8080)
