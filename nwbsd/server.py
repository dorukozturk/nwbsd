import base64

from flask import Flask
from flask import request
from flask_cors import CORS

from nwbsd import NwbSd
from PIL import Image

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/stimulus')
def stimulus():
    start = request.args.get('start')
    sd = NwbSd('/home/dorukozturk/Documents/nwbsd/tests/570014520.nwb')

    path = '/stimulus/presentation/natural_movie_one_stimulus'
    array = sd.getValueFromTimeStamp(path, float(start))
    image = Image.fromarray(array)

    return "data:image/png;base64,{}".format(base64.b64encode(image.tobytes()))
