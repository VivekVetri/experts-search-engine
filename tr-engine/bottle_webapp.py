from bottle import route, run, template, request, static_file
import metapy
from tabulate import tabulate

inv_idx = metapy.index.make_inverted_index('config.toml')


def decode_results(results):
    table_data = []
    for (docId, score) in results:
        with open("experts/experts.dat.names") as fp:
            for i, line in enumerate(fp):
                if i == docId:
                    table_data.append(",".join(line.split(','))+', '+str(score))

    return table_data


def remove_punctionations(text):
    for char in '-.,\n':
        text = text.replace(char, '')
    return text.lower()


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')


@route('/')
def root():
    return template('templates/index.html')


@route('/search', method='POST')
def search_keywords():
    # if request.method == 'GET':
    keywords = request.forms.get('query')
    print("Search query : ", keywords)

    # this line will try to load existing index or create new one if not exists
    # inv_idx = cache.get('inv_index')
    print("No. of docs in inv index : ", inv_idx.num_docs())
    print("No. of unique terms in inv index : ", inv_idx.unique_terms())
    print("Avg document length in inv index: ", inv_idx.avg_doc_length())
    print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

    query = metapy.index.Document()
    # orig_query = request.args.get('query')
    # orig_query = 'computer network'
    filtered = remove_punctionations(keywords)
    query.content(filtered)
    print("Search query : ", filtered)

    num_results = 5
    ranker = metapy.index.OkapiBM25(1.2, 0.75)
    # ranker = metapy.index.DirichletPrior()
    results = ranker.score(inv_idx, query, num_results)
    print("Top", num_results, "documents :")

    decoded_results = decode_results(results)
    print(decode_results)

    return template('templates/result.html', query=keywords, results=decoded_results)
    # return template('make_table', rows=results)


run(host='localhost', port=8080)
