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


if __name__ == '__main__':
    input_file = sys.argv[1]
    print("Reading input file ", input_file)

    if input_file is not None:
        with open(input_file, 'r') as fin:
            raw_data = json.load(fin)

        print("No. of records : ", len(raw_data))

        cleaned_data = []
        with open('data/experts.dat', 'w') as exp_dat:
            with open('data/experts.dat.names', 'w') as exp_dat_names:
                for profile in raw_data:
                    processed_details = process_details(profile.get('details'))
                    if processed_details:
                        name = profile.get('name', None)
                        page = profile.get('page', None)
                        if name is not None and page is not None:
                            name = remove_escape_sequences(name)
                            exp_dat_names.write(str(name)+' , '+str(page))
                            exp_dat_names.write('\n')
                            exp_dat.write(processed_details)
                            exp_dat.write('\n')

        exp_dat.close()
        exp_dat_names.close()
