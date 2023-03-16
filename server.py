from flask import Flask, request
import base64
import time
from cv import processHandPhoto

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/configure/nail_polisher", methods=['POST'])
def configure_polisher():
    img = request.form.get("img")
    img = img.replace(" ", "+")
    fN = str(time.time()) + ".jpg"
    with open(fN, "wb") as fh:
        fh.write(base64.b64decode(img))
    # TODO: For the future and better compliance, server shouldn't store data.
    # Also client side processing is easy with reduced number of libraries, when a migration project considered.
    # Because of the time constraints of the hackathon, we didn't do at the client-side.
    # For instance: mediapipe and opencv is mobile ready. Also there is some proprietary equivalents.
    response = processHandPhoto(fN)
    return response