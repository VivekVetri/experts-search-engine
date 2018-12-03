import time

import metapy
import pytoml
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

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate.
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index. You can ignore this for MP2.
    """
    # You can set your new InL2Ranker here by: return InL2Ranker(some_param=1.0)
    # Try to set the value between 0.9 and 1.0 and see what performs best
    # return metapy.index.JelinekMercer(0.09)
    # return metapy.index.AbsoluteDiscount(0.01)
    return metapy.index.DirichletPrior()
    # return InL2Ranker(some_param=0.9875)


@app.route('/', methods=['GET'])
def index():
    """ Builds index from the config.toml """
    if request.method == 'GET':
        path_prefix = "/app/backend/"
        cfg = path_prefix + "config.toml"
        idx = metapy.index.make_inverted_index(cfg)
        if not idx:
            print("Created index successfully ! ")
    return render_template('home.html')


def remove_punctionations(text):
    for char in '-.,\n':
        text = text.replace(char, '')
    return text.lower()


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # query = request.form['query']
        # print("Search query : ", query)
        query = metapy.index.Document()
        orig_query = str(request.form['query']).strip()
        filtered = remove_punctionations(orig_query)
        query.content(filtered)
        print("Search query : ", query.content())

        path_prefix = "/app/backend/"
        cfg = path_prefix + "config.toml"

        # this line will try to load existing index or create new one if not exists
        idx = metapy.index.make_inverted_index(cfg)

        ranker = load_ranker(cfg)
        print("ranker : ", ranker)

        result = ranker.score(idx, query, 1)
        print("Result : ", result)
    return render_template('result.html', query=orig_query, result=result)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
