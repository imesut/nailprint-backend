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
    response = processHandPhoto(img)
    return response