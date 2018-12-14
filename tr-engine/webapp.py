from bottle import route, run, template, request, static_file
from ranker import search, rebuild_index


def decode_results(results):
    """ Decodes the result by identifying the correct document """
    table_data = []
    for (docId, score) in results:
        with open("experts/experts.dat.names") as fp:
            for i, line in enumerate(fp):
                if i == docId:
                    table_data.append(",".join(line.split(',')) + ', ' + str(score))

    return table_data


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
    try:
        ranker_code = request.forms.getall('ranker_code')[0]
    except:
        # default bm25
        ranker_code = 'bm25'

    decoded_results = decode_results(search(ranker_code, keywords, 10, False))

    print("Ranker code : ", ranker_code)

    return template('templates/result.html', query=keywords, results=decoded_results, ranker_code=ranker_code)


# rebuild index on bootup
rebuild_index()

# runs the bottle app in port 8080
run(host='0.0.0.0', port=8080)
