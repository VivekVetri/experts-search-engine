import math
import sys
import time

import metapy


class PL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA
    """

    def __init__(self, c_param=0.5):
        self.c = c_param
        super(PL2Ranker, self).__init__()

    def score_one(self, sd):
        lda = sd.num_docs / sd.corpus_term_count
        tfn = sd.doc_term_count * math.log2(1.0 + self.c * sd.avg_dl /
                                            sd.doc_size)
        if lda < 1 or tfn <= 0:
            return 0.0
        numerator = tfn * math.log2(tfn * lda) \
                    + math.log2(math.e) * (1.0 / lda - tfn) \
                    + 0.5 * math.log2(2.0 * math.pi * tfn)
        return sd.query_term_weight * numerator / (tfn + 1.0)


if __name__ == '__main__':
    config = sys.argv[1]
    idx = metapy.index.make_inverted_index(config)
    idx = metapy.index.make_inverted_index(config)

    print("No. of documents : ", idx.num_docs())
    print("No. of unique terms : ", idx.unique_terms())
    print("Avg document length : ", idx.avg_doc_length())
    print("Total corpus terms : ", idx.total_corpus_terms())

    ranker = metapy.index.OkapiBM25()
    query = metapy.index.Document()
    query.content('computer network')
    ranker = PL2Ranker()
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
