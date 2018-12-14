import math
import shutil
import sys
from time import sleep

from tabulate import tabulate

import metapy

# supported rankers
supported_rankers = ['bm25', 'l2', 'jm', 'dp']


class L2Ranker(metapy.index.RankingFunction):
    """ New ranking function to use in ranker batch """

    def __init__(self, c_param=0.5):
        self.c = c_param
        super(L2Ranker, self).__init__()

    def score_one(self, s_d):
        lda = s_d.num_docs / s_d.corpus_term_count
        tfn = s_d.doc_term_count * math.log2(1.0 + self.c * s_d.avg_dl /
                                             s_d.doc_size)
        if lda < 1 or tfn <= 0:
            return 0.0
        numerator = tfn * math.log2(tfn * lda) \
                    + math.log2(math.e) * (1.0 / lda - tfn) \
                    + 0.5 * math.log2(2.0 * math.pi * tfn)
        return s_d.query_term_weight * numerator / (tfn + 1.0)


def decode_results(results):
    """ Decodes the result by finding the correct name, URL for given docID """
    table_data = []
    for (docId, score) in results:
        with open("experts/experts.dat.names") as fp:
            for i, line in enumerate(fp):
                if i == docId:
                    table_data.append(line.split(',') + [score])

    print(tabulate(table_data))


def rebuild_index():
    """ Rebuilds the index """
    inv_idx_dir = 'experts/idx'

    # remove the index directory for a fresh start
    try:
        shutil.rmtree(inv_idx_dir)
        sleep(2)
    except:
        pass

    return metapy.index.make_inverted_index('config.toml')


def search(ranker_code, keywords, num_results, refresh_index=False):
    """ Searches given keywords in index using the given ranker """
    if refresh_index:
        inv_idx = rebuild_index()

    # this will load the index if available
    inv_idx = metapy.index.make_inverted_index('config.toml')

    print("No. of docs in inv index : ", inv_idx.num_docs())
    print("No. of unique terms in inv index : ", inv_idx.unique_terms())
    print("Avg document length in inv index: ", inv_idx.avg_doc_length())
    print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

    # default ranker - bm25
    ranker = metapy.index.OkapiBM25(1.2, 0.75)

    if ranker_code in supported_rankers:
        if ranker_code == 'bm25':
            ranker = metapy.index.OkapiBM25(1.2, 0.75)
        elif ranker_code == 'l2':
            ranker = L2Ranker()
        elif ranker_code == 'jm':
            ranker = metapy.index.JelinekMercer(0.99)
        elif ranker_code == 'dp':
            ranker = metapy.index.DirichletPrior()

    print("Ranker :", ranker)
    query = metapy.index.Document()
    query.content(keywords)

    results = ranker.score(inv_idx, query, num_results)
    print("Top", num_results, "documents :")
    # decode_results(results)
    return results


def rank(config_file, ranker_code, refresh_cache=False):
    """ Ranks top documents for given query """
    if refresh_cache:
        inv_idx_dir = 'experts/idx'

        # remove the index directory for a fresh start
        try:
            shutil.rmtree(inv_idx_dir)
            sleep(2)
        except:
            pass

    # this will load the index if available
    inv_idx = metapy.index.make_inverted_index(config_file)

    print("No. of docs in inv index : ", inv_idx.num_docs())
    print("No. of unique terms in inv index : ", inv_idx.unique_terms())
    print("Avg document length in inv index: ", inv_idx.avg_doc_length())
    print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

    # default ranker - bm25
    ranker = metapy.index.OkapiBM25(1.2, 0.75)

    if ranker_code in supported_rankers:
        if ranker_code == 'bm25':
            ranker = metapy.index.OkapiBM25(1.2, 0.75)
        elif ranker_code == 'l2':
            ranker = L2Ranker()
        elif ranker_code == 'jm':
            ranker = metapy.index.JelinekMercer(0.99)
        elif ranker_code == 'dp':
            ranker = metapy.index.DirichletPrior()

    print("Ranker :", ranker)
    query = metapy.index.Document()

    print("\nIR Evaluation : ")
    # IR Evaluation
    eval = metapy.index.IREval(config)
    num_results = 5
    with open('experts/experts-queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query_keywords = line.strip()
            print(80 * '*')
            print('\t\t\tQuery', query_num + 1, ':', query_keywords)
            print(80 * '*')
            query.content(query_keywords)

            results = ranker.score(inv_idx, query, num_results)
            avg_p = eval.avg_p(results, query_num, num_results)
            f1 = eval.f1(results, query_num, num_results)
            recall = eval.recall(results, query_num, num_results)
            precision = eval.precision(results, query_num, num_results)
            ndcg = eval.ndcg(results, query_num, num_results)

            print("Top", num_results, "documents :")
            decode_results(results)

            print(
                "Average precision: {} \noverall recall : {} \noverall f1 score : {} \nndcg : {}\nprecision : {}".format(
                    avg_p, recall, f1, ndcg, precision))
            print(80 * '-')

    print("\nMAP : ", eval.map())


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: {} config.toml [bm25]".format(sys.argv[0]))
        print("Supported rankers :", supported_rankers)
        sys.exit(1)

    config = sys.argv[1]
    try:
        ranker_id = sys.argv[2]
    except:
        # default bm25
        ranker_id = 'bm25'

    # rank the documents
    rank(config, ranker_id, True)
