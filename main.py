from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections


def get_excel_wines():
    '''Возвращает словарь с данными о вине полученным из Excel файла клиента'''

    excel_wines = pandas.read_excel('wines.xlsx', na_values='some_dummy_na_value', keep_default_na=False)
    wines = excel_wines.to_dict(orient='records')
    wines_dict = collections.defaultdict(list)
    for i in wines:
        wines_dict[i['Категория']].append(i)
    # pprint(wines_dict)
    return wines_dict


def days_with_you():
    '''Возвращает кол-во лет компании'''

    date_start = datetime.datetime(year=1920, month=1, day=1, hour=0)
    today = datetime.datetime.now()
    years = today.year - date_start.year
    if years % 100 in [11, 12, 13, 14]:  # функция возвращает слово год в правильной форме в зависимости от окончания
        return f'{years} лет'
    if years % 10 == 1:
        return f'{years} год'
    elif 0 < years % 10 < 5:
        return f'{years} года'
    return f'{years} лет'


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(days_with_you=days_with_you(), wines_dict=get_excel_wines())

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
