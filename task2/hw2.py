import os
import re

from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
from pymorphy3 import MorphAnalyzer
from collections import defaultdict
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('snowball_data')
nltk.download('perluniprops')
nltk.download('universal_tagset')
nltk.download('nonbreaking_prefixes')
nltk.download('wordnet')

stop_words = stopwords.words('russian') + stopwords.words('english')
DIRECTORY = "C:/Users/alex1/OneDrive/Desktop/homework1/выкачка"


def get_tokens(text):
    # токенизатор на регулярных выражениях
    tokenizer = RegexpTokenizer('[А-Яа-яёЁ]+')
    clean_words = tokenizer.tokenize(text)
    clean_words = [w.lower() for w in clean_words if w != '']
    clean_words = [w for w in clean_words if w not in stop_words]
    return set(clean_words)


def get_lemmas(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = []
    for token in tokens:
        if re.match(r'[А-Яа-яёЁ]', token):
            lemma = pymorphy2_analyzer.parse(token)[0].normal_form
            lemmas.append(lemma)
    return lemmas


def get_lemmas_dict(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = defaultdict(list)
    for token in tokens:
        if re.match(r'[А-Яа-яёЁ]', token):
            lemma = pymorphy2_analyzer.parse(token)[0].normal_form
            lemmas[lemma].append(token)
    return lemmas


def get_for_every_file():
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith('.txt'):
                path_file = os.path.join(root, file)
                with open(path_file, encoding="utf-8") as f:
                    html_text = f.read()
                soup = BeautifulSoup(html_text, "html.parser")
                text = ' '.join(soup.stripped_strings)
                tokens = get_tokens(text)
                tokens_string = '\n'.join(tokens)
                path_result = f"Для каждого файла/tokens_{file}"
                os.makedirs(os.path.dirname(path_result), exist_ok=True)
                with open(path_result, "w", encoding="utf-8") as file_result:
                    file_result.write(tokens_string)
                lemmas_dict = get_lemmas(tokens)
                path_result = f"Для каждого файла/lemmas_{file}"
                with open(path_result, "w", encoding="utf-8") as file_result:
                    for k in lemmas_dict:
                        file_result.write(k + '\n')
                        # for word in v:
                        #     file_result.write(word + " ")
                        # file_result.write("\n")


def get_common():
    tokens = []
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith('.txt'):
                path_file = os.path.join(root, file)
                with open(path_file, encoding="utf-8") as f:
                    html_text = f.read()
                soup = BeautifulSoup(html_text, "html.parser")
                text = ' '.join(soup.stripped_strings)
                tokens += get_tokens(text)
    tokens = list(set(tokens))
    tokens_string = '\n'.join(tokens)
    path_result = f"Результаты/tokens.txt"
    os.makedirs(os.path.dirname(path_result), exist_ok=True)
    with open(path_result, "w", encoding="utf-8") as file_result:
        file_result.write(tokens_string)
    lemmas_dict = get_lemmas_dict(tokens)
    path_result = f"Результаты/lemmas.txt"
    with open(path_result, "w", encoding="utf-8") as file_result:
        for k, v in lemmas_dict.items():
            file_result.write(k + ": ")
            for word in v:
                file_result.write(word + " ")
            file_result.write("\n")


if __name__ == '__main__':
    # get_for_every_file()
     get_common()