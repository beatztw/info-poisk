import json
import requests
from bs4 import BeautifulSoup
import os

MAIN_LINK = 'https://ru.wikipedia.org/wiki/Википедия:Список_хороших_статей/'
BASE_URL = 'https://ru.wikipedia.org'
COUNT_PAGES = 100
INFO_FILE = 'index.txt'

index = {}

def get_links(url):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, features="lxml")
    links = []
    for row in soup.find('table', {'class': 'standard'}).find_all('tr'):
        href = row.find_next('a').get('href')
        if href:
            links.append(f'{BASE_URL}{href}')
    return links

def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script', 'noscript', 'link']):
        data.decompose()
    return str(soup)

def crawl(url):
    page = requests.get(url)
    data = page.text
    return remove_tags(data)

def save_index(text_file_path):
    dump = json.dumps(index,
                      sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))
    with open(text_file_path, "w") as f:
        f.write(dump)

if __name__ == '__main__':
    links_all = []
    info_string = ""
    year = 2022

    # Собираем ссылки, пока не наберем 100
    while len(links_all) < COUNT_PAGES and year <= 2023:  # Ограничиваем год, чтобы не уйти в бесконечный цикл
        current_link = f'{MAIN_LINK}{year}'
        print(f"Парсинг года: {year}")
        links = get_links(current_link)
        links_all.extend(links)
        year += 1

    # Обрезаем список до 100 ссылок, если их больше
    links_all = links_all[:COUNT_PAGES]

    # Скачиваем и сохраняем статьи
    for i, link in enumerate(links_all):
        print(f"Скачивание статьи {i + 1}/{len(links_all)}: {link}")
        html_text = crawl(link)
        index[i] = link
        filename = f'{i+1}'
        info_string += f"{filename}\t{link}\n"
        path_result = f"выкачка/{filename}.txt"
        os.makedirs(os.path.dirname(path_result), exist_ok=True)
        with open(path_result, "w", encoding="utf-8") as file_result:
            file_result.write(html_text)

    # Сохраняем индекс
    with open(INFO_FILE, "w", encoding="utf-8") as f:
        f.write(info_string)
    save_index('index.json')

    print(f"Скачано {len(links_all)} статей.")