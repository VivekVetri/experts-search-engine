from flask import Flask, request, render_template

import sys
import metapy
import pytoml
from tabulate import tabulate

app = Flask(__name__)


def decode_results(results):
    table_data = []
    for (docId, score) in results:
        with open("experts/experts.dat.names") as fp:
            for i, line in enumerate(fp):
                if i == docId:
                    table_data.append(line.split(','))

    print(tabulate(table_data))


def remove_punctionations(text):
    for char in '-.,\n':
        text = text.replace(char, '')
    return text.lower()


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # query = request.form['query']
        # print("Search query : ", query)

        # this line will try to load existing index or create new one if not exists
        inv_idx = metapy.index.make_inverted_index('config.toml')
        # inv_idx = cache.get('inv_index')
        print("No. of docs in inv index : ", inv_idx.num_docs())
        print("No. of unique terms in inv index : ", inv_idx.unique_terms())
        print("Avg document length in inv index: ", inv_idx.avg_doc_length())
        print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

        query = metapy.index.Document()
        orig_query = request.form['query']
        filtered = remove_punctionations(orig_query)
        query.content(filtered)
        print("Search query : ", filtered)

        num_results = 5
        # ranker = metapy.index.OkapiBM25(1.2, 0.75)
        ranker = metapy.index.DirichletPrior()
        results = ranker.score(inv_idx, query, num_results)
        print("Top", num_results, "documents :")
        decode_results(results)
        print(results)

    return render_template('result.html', query=orig_query, result=results)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]

    idx = metapy.index.make_inverted_index(cfg)
    if idx:
        # rv = cache.set(key='inv_index', value=idx)
        # if rv:
        print("Created index successfully ! Cached !")

    # server(sys.argv[1]).run(debug=True)
    app.run(host='127.0.0.1', debug=True, port=8080)
