import sys

import metapy

if __name__ == '__main__':
    config = sys.argv[1]
    idx = metapy.index.make_inverted_index(config)

    print("No. of documents : ", idx.num_docs())
    print("No. of unique terms : ", idx.unique_terms())
    print("Avg document length : ",  idx.avg_doc_length())
    print("Total corpus terms : ", idx.total_corpus_terms())

    ranker = metapy.index.OkapiBM25()
    query = metapy.index.Document()
    query.content('computer network')
    top_docs = ranker.score(idx, query, num_results=5)
    print(top_docs)

    # for num, (d_id, _) in enumerate(top_docs):
    #     content = idx.metadata(d_id).get('content')
    #     print("{}. {}...\n".format(num + 1, content[0:250]))

    # IR Evaluation
    ev = metapy.index.IREval(config)
    num_results = 10
    with open('experts/experts-queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, num_results)
            avg_p = ev.avg_p(results, query_num, num_results)
            print("Query {} average precision: {}".format(query_num + 1, avg_p))

    print("MAP : ", ev.map())
