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


@app.route('/', methods=['GET', 'POST'])
def index():
    path_prefix = "/app/backend/"
    if request.method == 'POST':
        pass

    start_time = time.time()
    cfg = path_prefix + "config.toml"
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    query_cfg = cfg_d['query-runner']
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    top_k = 10

    query = metapy.index.Document()
    print('Running queries')
    with open(path_prefix + 'inl2.avg_p.txt', 'a') as file:
        with open(query_path) as query_file:
            for query_num, line in enumerate(query_file):
                query.content(line.strip())
                results = ranker.score(idx, query, top_k)
                avg_p = ev.avg_p(results, query_start + query_num, top_k)
                print("Query {} average precision: {}".format(query_num + 1, avg_p))
                file.write(str(avg_p) + "\n")
    print("Mean average precision: {}".format(ev.map()))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
    return render_template('home.html')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
