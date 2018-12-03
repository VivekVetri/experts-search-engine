import codecs
import sys
import json
import re
from pprint import pprint

from nltk.corpus import stopwords


def remove_tags(html_text):
    xml_tag_regex = re.compile(r'<[^>]+>')
    return xml_tag_regex.sub('', html_text)


def remove_escape_sequences(text):
    text_without_es = text.replace('\t', '').replace('\n', '').replace('\r', '')
    return re.sub(r'[^\w]', ' ', text_without_es)


def getWords(text):
    return re.compile('\w+').findall(text)


def process_details(input_text):
    html_string = " ".join(input_text)
    plain_string = remove_tags(html_string).lower()
    cleaned_string = remove_escape_sequences(plain_string)
    filtered_string_list = [word for word in cleaned_string.split(' ') if word not in stopwords.words('english')]
    filtered_string = " ".join(filtered_string_list)
    output_text = " ".join(getWords(filtered_string))
    return output_text


if __name__ == '__main__':
    input_file = sys.argv[1]
    print("Reading input file ", input_file)

    if input_file is not None:
        with open(input_file, 'r') as fin:
            raw_data = json.load(fin)

        print("No. of records : ", len(raw_data))

        cleaned_data = []
        for profile in raw_data:
            cleaned_data.append({'page': profile.get('page', None),
                                 'name': profile.get('page', None),
                                 'details': process_details(profile.get('details', []))})

        # pprint(cleaned_data[0:5])

        output_file = sys.argv[2]

        print("Writing results to ", output_file)

        with open(output_file, 'w') as fout:
            json.dump(cleaned_data, fout, indent=4)
            # json.dumps(cleaned_data, fout)

        fin.close()
        fout.close()
