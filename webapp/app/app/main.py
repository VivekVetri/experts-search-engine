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


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        pass

    cfg = "/app/backend/config.toml"
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    print('Running queries')
    with open('inl2.avg_p.txt', 'a') as file:
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
