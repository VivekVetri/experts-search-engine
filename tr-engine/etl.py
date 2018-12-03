import sys
import json
import re

from nltk.corpus import stopwords


def remove_tags(html_text):
    xml_tag_regex = re.compile(r'<[^>]+>')
    return xml_tag_regex.sub(' ', html_text)


def remove_escape_sequences(text):
    text_without_es = text.replace('\t', '').replace('\n', '').replace('\r', '')
    return re.sub(r'[^\w]', ' ', text_without_es)


def get_words(text):
    return re.compile('\w+').findall(text)


def process_details(input_text):
    html_string = " ".join(input_text)
    plain_string = remove_tags(html_string).lower()
    cleaned_string = remove_escape_sequences(plain_string)
    filtered_string_list = [word for word in cleaned_string.split(' ') if word not in stopwords.words('english')]
    filtered_string = " ".join(filtered_string_list)
    output_text = " ".join(get_words(filtered_string))
    return output_text


def write_to_file(input_list, output_file):
    with open(output_file, 'w') as f:
        for item in input_list:
            f.write("%s\n" % item)
    f.close()


if __name__ == '__main__':
    input_file = sys.argv[1]

    experts_data_file = 'tr-engine/experts/experts.dat'
    experts_data_names_file = 'tr-engine/experts/experts.dat.names'
    experts_queries_file = 'tr-engine/experts/experts-queries.txt'
    experts_qrels_file = 'tr-engine/experts/experts-qrels.txt'

    print("Reading input file ", input_file)

    if input_file is not None:
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
                    if processed_details:
                        name = profile.get('name', None)
                        page = profile.get('page', None)
                        if name is None:
                            name = 'N/A'
                        if name is not None and page is not None:
                            name = remove_escape_sequences(name)
                            valid_records += 1
                            exp_dat_names.write(str(name) + ' , ' + str(page))
                            exp_dat_names.write('\n')
                            exp_dat.write(processed_details)
                            exp_dat.write('\n')

        print("No. of valid records :", valid_records)

        exp_dat.close()
        exp_dat_names.close()

    rel_judgement_file = sys.argv[2]

    if rel_judgement_file is not None:
        print("Generating ", experts_queries_file, experts_qrels_file, "...")

        with open(rel_judgement_file, 'r') as rjf_in:
            rel_content = rjf_in.readlines()
        rel_content = [line.strip() for line in rel_content]

        with open(experts_data_names_file, 'r') as edn_in:
            url_content = edn_in.readlines()

        url_content = [line.strip() for line in url_content]

        query_keywords_set = set()
        result_url_list = []
        for rel in rel_content:
            keywords, result_url, relevance = rel.split(',')
            formatted_keywords = keywords.lower().strip()
            formatted_result_url = result_url.lower().strip()
            if formatted_result_url and formatted_keywords:
                query_keywords_set.add(formatted_keywords)
                result_url_list.append(formatted_result_url)

        query_keywords_list = list(query_keywords_set)
        # print("Query keywords :", query_keywords_list)
        # print("urls :", result_url_list)

        qrels_list = []
        rels_counter = 0
        for rel in rel_content:
            keywords, result_url, relevance = rel.split(',')
            formatted_keywords = keywords.lower().strip()
            formatted_result_url = result_url.lower().strip()
            if formatted_keywords and formatted_result_url and str(relevance):
                try:
                    qrel = str(str(query_keywords_list.index(formatted_keywords)) + ' ' + str(
                        result_url_list.index(formatted_result_url)) + ' ' + str(relevance).strip())
                    qrels_list.append(qrel)
                    rels_counter += 1
                except:
                    pass

        # print("Result : ")
        # for qrel in qrels_list:
        #     print(qrel)

        write_to_file(query_keywords_list, experts_queries_file)
        write_to_file(qrels_list, experts_qrels_file)
        print("No. of unique queries generated :", len(query_keywords_list))
        print("No. of relevance judgmentments generated :", rels_counter)
