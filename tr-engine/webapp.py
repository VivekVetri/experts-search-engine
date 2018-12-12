from bottle import route, run, template, request, static_file
import metapy

# Build inverted index
inv_idx = metapy.index.make_inverted_index('config.toml')


def decode_results(results):
    """ Decodes the result by identifying the correct document """
    table_data = []
    for (docId, score) in results:
        with open("experts/experts.dat.names") as fp:
            for i, line in enumerate(fp):
                if i == docId:
                    table_data.append(",".join(line.split(',')) + ', ' + str(score))

    return table_data


def remove_punctuations(text):
    """ Cleans up text """
    for charac in '-.,\n':
        text = text.replace(charac, '')
    return text.lower()


@route('/static/<filepath:path>')
def server_static(filepath):
    """ Serving the static files """
    return static_file(filepath, root='./static/')


@route('/')
def root():
    """ Home page """
    return template('templates/index.html')


@route('/search', method='POST')
def search_keywords():
    """ Search results page accepting POST requests """
    """ Sample request - { 'query' : 'computer science' }"""

    keywords = request.forms.get('query')

    # this line will try to load existing index or create new one if not exists
    # inv_idx = cache.get('inv_index')

    # Summary of inverted index
    print("No. of docs in inv index : ", inv_idx.num_docs())
    print("No. of unique terms in inv index : ", inv_idx.unique_terms())
    print("Avg document length in inv index: ", inv_idx.avg_doc_length())
    print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

    query = metapy.index.Document()

    filtered = remove_punctuations(keywords)
    query.content(filtered)

    print("Search query : ", filtered)

    # top results
    num_results = 10

    ranker = metapy.index.OkapiBM25(1.2, 0.75)
    # ranker = metapy.index.DirichletPrior()
    results = ranker.score(inv_idx, query, num_results)

    print("Top", num_results, "documents :")

    decoded_results = decode_results(results)
    for result in decoded_results:
        print(result)

    return template('templates/result.html', query=keywords, results=decoded_results)


# runs the bottle app in port 8080
run(host='0.0.0.0', port=8080)
