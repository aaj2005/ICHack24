"""
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

#########
""" 
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from terra.base_client import Terra
import requests
import uvicorn
import datetime

app = FastAPI()

# replace this with the root url for your app,
# http://127.0.0.1:8000 if you're doing it locally or
# use ngrok to generate a link like the one below :)
base_url = 'https://5332-2a0c-5bc0-40-2e30-7c5a-c503-d505-ea6d.ngrok-free.app'



API_KEY = "O8sTDuQBXJfQDlULKMZrnOKlzzRNHMpi"
DEV_ID = "ichack-testing-cgyBGcj290"
SECRET = "4edcc0dfbabb6a58094bcdf64c51595d7161773fcd6a267b"


terra = Terra(API_KEY, DEV_ID, SECRET) 
"""

# USER_ID = "e036976a-027d-4eb2-8b9f-22ae3afbb382"
# terra_user = terra.from_user_id(USER_ID)


    

@app.get('/login')
async def auth():    
    # generates a widget to be shown to the user

    res = requests.post('https://api.tryterra.co/auth/generateWidgetSession',
        headers={ 
            'dev-id': DEV_ID, 
            'x-api-key': API_KEY
        },
        json={
            'reference_id': 'john',
            'auth_success_redirect_url': f'{base_url}/on_auth_success', # after the user finishes connecting, we send em here
        }
        
    )
    

    data = res.json()
    url = data['url']
    print(url)
    return RedirectResponse(url)


    

# The user will be sent here after auth
@app.post('/consumeTerraWebhook')
async def consume_terra_webhook():
    # body_str = str(request.get_data(), 'utf-8')
    body = requests.get_json()
    
    print(body)
    # ML to be inserted
    _LOGGER.info(
        "Received webhook for user %s of type %s",
        body.get("user", {}).get("user_id"),
        user_id = body.get("user", {}).get("user_id")

        body["type"])
    verified = terra.check_terra_signature(requests.get_data().decode("utf-8"), requests.headers['terra-signature'])
    if verified:
      return "verified"
    else:
      return "not verified"

    # test getting data for the new user_id
    # you can also just store the user_id for later

"""

user_id = "e3e545ea-e2b3-4903-940b-ab0b6f5fce9e"
 
Date_start = 0#get date for graphs
Date_end = 0#get data for graphs
Current_date= datetime.datetime.now()
start_data = "2022-10-01"
end_data = "2022-10-01"
webhook = "true"
samples = 'true'

print(Current_date)

url = "https://api.tryterra.co/v2/sleep?user_id="+user_id+"&start_date="+start_data+"&end_date="+end_data+"&to_webhook="+webhook+"&with_samples="+samples
print(url)

headers = {
    "accept": "application/json",
    "dev-id": DEV_ID,
    "x-api-key": API_KEY
}

response = requests.get(url, headers=headers)



# After your done, go to {base_url}/login to start using your
# app.
# Can't wait to see what you build!!!
"""
if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8080, log_level="info")
"""