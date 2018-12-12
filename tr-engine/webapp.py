import shutil
from time import sleep

from bottle import route, run, template, request, static_file
import metapy
from ranker import search


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
    try:
        ranker_code = request.forms.getall('ranker_code')[0]
    except:
        ranker_code = 'bm25'
    decoded_results = decode_results(search(ranker_code, keywords, 10, False))
    print("Ranker code : ", ranker_code)

    return template('templates/result.html', query=keywords, results=decoded_results, ranker_code=ranker_code)


# runs the bottle app in port 8080
run(host='0.0.0.0', port=8080)
