from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from config import SETTING_PATH


def get_excel_wines():
    '''Возвращает словарь с данными о вине полученным из Excel файла клиента'''

    excel_wines = pandas.read_excel(SETTING_PATH, na_values='some_dummy_na_value', keep_default_na=False)
    wines = excel_wines.to_dict(orient='records')
    wine_cluster = collections.defaultdict(list)
    for i in wines:
        wine_cluster[i['Категория']].append(i)
    return wine_cluster


def get_right_ending_word_year(company_age):
    if company_age % 100 in [11, 12, 13, 14]:
        return 'лет'
    elif company_age % 10 == 1:
        return 'год'
    elif 0 < company_age % 10 < 5:
        return 'года'
    return 'лет'


def get_company_age():
    '''Возвращает кол-во лет компании'''

    year_start = 1920
    today = datetime.datetime.now()
    company_age = today.year - year_start
    word_year_in_ru = get_right_ending_word_year(company_age)
    return f'{company_age} {word_year_in_ru}'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(company_age=get_company_age(), wines_dict=get_excel_wines())

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
