from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections

excel_wines = pandas.read_excel('wine3.xlsx', na_values='some_dummy_na_value', keep_default_na=False)
wines = excel_wines.to_dict(orient='records')
wines_dict = collections.defaultdict(list)
for i in wines:
    wines_dict[i['Категория']].append(i)
    # if i['Категория'] in slovar.keys():
    #     slovar[i['Категория']].append(i)
    # else:
    #     slovar[i['Категория']] = [i]
pprint(len(wines_dict.keys()))
pprint(wines)
for i in wines_dict:
    print(i)



def days_with_you():
    '''Возвращает кол-во лет компании'''

    date_start = datetime.datetime(year=1920, month=1, day=1, hour=0)
    today = datetime.datetime.now()
    years = today.year - date_start.year
    if years % 100 in [11,12,13,14]:
        return f'{years} лет'
    if years % 10 == 1:             # функция возвращает слово год в правильной форме в зависимости от окончания
        return f'{years} год'
    elif 0 < years % 10 < 5:
        return f'{years} года'
    return f'{years} лет'


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(days_with_you=days_with_you(), wines=wines, wines_dict=wines_dict)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
