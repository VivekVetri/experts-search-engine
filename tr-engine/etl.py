import sys
import json
import re
from orderedset import OrderedSet


def remove_tags(html_text):
    """ Removes XML/HTML tags """
    xml_tag_regex = re.compile(r'<[^>]+>')
    return xml_tag_regex.sub(' ', html_text)


def remove_escape_sequences(text):
    """ Removes escape sequences """
    text_without_es = text.replace('\t', '').replace('\n', '').replace('\r', '')
    return re.sub(r'[^\w]', ' ', text_without_es)


def get_words(text):
    """ Returns list of words skipping whitespaces """
    return re.compile('\w+').findall(text)


def process_details(input_text):
    """ Processes the raw details from crawler """
    html_string = " ".join(input_text)
    plain_string = remove_tags(html_string).lower()
    cleaned_string = remove_escape_sequences(plain_string)
    output_text = " ".join(get_words(cleaned_string))
    return output_text


def write_to_file(input_list, output_file):
    """ Writes a list line-by-line to a file """
    with open(output_file, 'w') as f:
        for item in input_list:
            f.write("%s\n" % item)
    f.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} expert.json expert-queries.csv".format(sys.argv[0]))
        sys.exit(1)

    # Input json from crawler
    input_file = sys.argv[1]

    # Experts Dataset
    dataset_prefix = 'tr-engine/experts'
    experts_data_file = dataset_prefix + '/experts.dat'
    experts_data_names_file = dataset_prefix + '/experts.dat.names'
    experts_queries_file = dataset_prefix + '/experts-queries.txt'
    experts_qrels_file = dataset_prefix + '/experts-qrels.txt'

    print("Reading input file ", input_file)

    page_url_list_data = []
    if input_file is not None:
        # Loading input json as dictionary
        with open(input_file, 'r') as fin:
            raw_data = json.load(fin)

        print("No. of input records : ", len(raw_data))

        cleaned_data = []

        print("Generating ", experts_data_file, experts_data_names_file, "...")
        valid_records = 0

        with open(experts_data_file, 'w') as exp_dat:
            with open(experts_data_names_file, 'w') as exp_dat_names:
                for profile in raw_data:
                    processed_details = process_details(profile.get('details'))

                    # only if details has data
                    if processed_details:
                        name = profile.get('name', None)
                        page = profile.get('page', None)

                        # page url is mandatory
                        if page is not None:
                            if name is None:
                                name = 'N/A'
                            elif name is not None:
                                name = remove_escape_sequences(name)
                            valid_records += 1

                            # experts.dat.names file
                            exp_dat_names.write(str(name) + ' , ' + str(page))
                            exp_dat_names.write('\n')
                            page_url_list_data.append(page.lower().strip())

                            # experts.dat file
                            exp_dat.write(processed_details)
                            exp_dat.write('\n')

        print("No. of valid records :", valid_records)

        exp_dat.close()
        exp_dat_names.close()

    # Judgements csv file - query words, documentID, 1/0
    rel_judgement_file = sys.argv[2]

    if rel_judgement_file is not None:
        print("Generating ", experts_queries_file, experts_qrels_file, "...")

        # Load the judgements csv file
        with open(rel_judgement_file, 'r') as rjf_in:
            rel_content = rjf_in.readlines()

        rel_content = [line.strip() for line in rel_content]

        # Query keywords to store unique set of query keywords
        query_keywords_set = OrderedSet()

        result_url_list = []

        for rel in rel_content:
            keywords, result_url, relevance = rel.split(',')
            formatted_keywords = keywords.lower().strip()
            formatted_result_url = result_url.lower().strip()

            # Store unique keywords in set and documentID / page url into a list
            if formatted_result_url and formatted_keywords:
                query_keywords_set.add(formatted_keywords)
                result_url_list.append(formatted_result_url)

        query_keywords_list = list(query_keywords_set)

        # print("Query keywords :", query_keywords_list)
        # print("urls :", result_url_list)

        qrels_list = []
        rels_counter = 0
        skip_counter = 0

        # second parse over relevance judgements to find the correct indices of query words and docID
        for rel in rel_content:
            # get query keywords, docID / page url, relevance from each document
            keywords, result_url, relevance = rel.split(',')

            formatted_keywords = keywords.lower().strip()
            formatted_result_url = result_url.lower().strip()

            # only if all three info is available
            if formatted_keywords and formatted_result_url and str(relevance):
                qrel = str(str(query_keywords_list.index(formatted_keywords)) + ' '
                           + str(page_url_list_data.index(formatted_result_url)) + ' '
                           + str(relevance).strip())
                qrels_list.append(qrel)
                rels_counter += 1
            else:
                # skip if there is any missing data
                skip_counter += 1

        # experts-queries.txt
        write_to_file(query_keywords_list, experts_queries_file)

        # experts-qrels.txt
        write_to_file(qrels_list, experts_qrels_file)

        print("No. of unique queries generated :", len(query_keywords_list))
        print("No. of relevance judgmentments generated :", rels_counter)
        print("No. of relevance judgmentments skipped :", skip_counter)
