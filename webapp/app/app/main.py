from flask import Flask, request, abort, jsonify, logging, render_template
from pymongo import MongoClient
import requests
from requests.auth import HTTPBasicAuth
from flask_basicauth import BasicAuth

app = Flask(__name__)


# app.config['BASIC_AUTH_USERNAME'] = 'ese'
# app.config['BASIC_AUTH_PASSWORD'] = 'ExpertSearchEngine'

# enforcing authentication on entire app
# app.config['BASIC_AUTH_FORCE'] = True

# basic_auth = BasicAuth(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    return render_template('home.html')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
