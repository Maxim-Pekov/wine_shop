from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os
from dotenv import load_dotenv

BASE_PATH = 'wines.xlsx'


def get_excel_wines():
    '''Возвращает словарь с данными о напитках полученным из Excel файла клиента'''

    SETTING_PATH = os.getenv('SETTING_PATH', BASE_PATH)
    excel_wines = pandas.read_excel(SETTING_PATH, na_values='some_dummy_na_value', keep_default_na=False)
    wines = excel_wines.to_dict(orient='records')
    wine_cluster = collections.defaultdict(list)
    for wine in wines:
        wine_cluster[wine['Категория']].append(wine)
    return wine_cluster


def get_correct_form_of_the_word(company_age):
    if company_age % 100 in [11, 12, 13, 14]:
        return 'лет'
    elif company_age % 10 == 1:
        return 'год'
    elif 0 < company_age % 10 < 5:
        return 'года'
    return 'лет'


def get_company_age():
    '''Возвращает кол-во лет компании'''

    year_of_foundation = 1920
    today = datetime.datetime.now()
    company_age = today.year - year_of_foundation
    correct_form_of_the_word = get_correct_form_of_the_word(company_age)
    return f'{company_age} {correct_form_of_the_word}'


def main():
    load_dotenv()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(company_age=get_company_age(), wine_cluster=get_excel_wines())

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
