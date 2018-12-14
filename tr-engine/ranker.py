import math
import shutil
import sys
from time import sleep

from tabulate import tabulate

import metapy

supported_rankers = ['bm25', 'l2', 'jm', 'dp']


class InL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA
    """

    def __init__(self, c_param=0.5):
        self.c = c_param
        super(InL2Ranker, self).__init__()

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


def decode_results(results):
    table_data = []
    for (docId, score) in results:
        with open("experts/experts.dat.names") as fp:
            for i, line in enumerate(fp):
                if i == docId:
                    table_data.append(line.split(',') + [score])

    print(tabulate(table_data))


def rebuild_index():
    inv_idx_dir = 'experts/idx'

    # remove the index directory for a fresh start
    try:
        shutil.rmtree(inv_idx_dir)
        sleep(2)
    except:
        pass

    return metapy.index.make_inverted_index('config.toml')


def search(ranker_code, keywords, num_results, refresh_index=False):
    if refresh_index:
        inv_idx = rebuild_index()

    inv_idx = metapy.index.make_inverted_index('config.toml')

    print("No. of docs in inv index : ", inv_idx.num_docs())
    print("No. of unique terms in inv index : ", inv_idx.unique_terms())
    print("Avg document length in inv index: ", inv_idx.avg_doc_length())
    print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

    # default ranker - bm25
    ranker = metapy.index.OkapiBM25(1.2, 0.75)

    # if len(sys.argv) == 3:
    #     ranker_code = str(sys.argv[2]).strip().lower()
    # else:
    #     ranker_code = 'bm25'

    if ranker_code in supported_rankers:
        if ranker_code == 'bm25':
            ranker = metapy.index.OkapiBM25(1.2, 0.75)
        elif ranker_code == 'l2':
            ranker = InL2Ranker()
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
    if refresh_cache:
        inv_idx_dir = 'experts/idx'

        # remove the index directory for a fresh start
        try:
            shutil.rmtree(inv_idx_dir)
            sleep(2)
        except:
            pass

    inv_idx = metapy.index.make_inverted_index(config_file)

    print("No. of docs in inv index : ", inv_idx.num_docs())
    print("No. of unique terms in inv index : ", inv_idx.unique_terms())
    print("Avg document length in inv index: ", inv_idx.avg_doc_length())
    print("Total corpus terms in inv index : ", inv_idx.total_corpus_terms())

    # default ranker - bm25
    ranker = metapy.index.OkapiBM25(1.2, 0.75)

    # if len(sys.argv) == 3:
    #     ranker_code = str(sys.argv[2]).strip().lower()
    # else:
    #     ranker_code = 'bm25'

    if ranker_code in supported_rankers:
        if ranker_code == 'bm25':
            ranker = metapy.index.OkapiBM25(1.2, 0.75)
        elif ranker_code == 'l2':
            ranker = InL2Ranker()
        elif ranker_code == 'jm':
            ranker = metapy.index.JelinekMercer(0.99)
        elif ranker_code == 'dp':
            ranker = metapy.index.DirichletPrior()

    print("Ranker :", ranker)
    query = metapy.index.Document()

    print("\nIR Evaluation : ")
    # IR Evaluation
    ev = metapy.index.IREval(config)
    num_results = 5
    with open('experts/experts-queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query_keywords = line.strip()
            print(80 * '*')
            print('\t\t\tQuery', query_num + 1, ':', query_keywords)
            print(80 * '*')
            query.content(query_keywords)

            results = ranker.score(inv_idx, query, num_results)
            avg_p = ev.avg_p(results, query_num, num_results)
            f1 = ev.f1(results, query_num, num_results)
            recall = ev.recall(results, query_num, num_results)
            precision = ev.precision(results, query_num, num_results)
            ndcg = ev.ndcg(results, query_num, num_results)

            print("Top", num_results, "documents :")
            decode_results(results)

            print(
                "Average precision: {} \noverall recall : {} \noverall f1 score : {} \nndcg : {}\nprecision : {}".format(
                    avg_p, recall, f1, ndcg, precision))
            print(80 * '-')

    print("\nMAP : ", ev.map())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} config.toml [bm25]".format(sys.argv[0]))
        print("Supported rankers :", supported_rankers)
        sys.exit(1)
    config = sys.argv[1]
    try:
        ranker_id = sys.argv[2]
    except:
        ranker_id = 'bm25'

    rank(config, ranker_id, True)
