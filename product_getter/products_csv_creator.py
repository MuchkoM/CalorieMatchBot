import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

url = 'https://calorizator.ru/product/all?page={}'
pages = range(0, 75)

data = {
    'name': [],
    'fat': [],
    'protein': [],
    'carbohydrates': [],
    'kcal': [],

}


def to_zero(value):
    if not value:
        return '0'
    else:
        return value


with requests.Session() as session:
    for i in pages:
        print('page {} '.format(i), end='')
        r = session.get(url.format(i))
        if r.status_code != 200:
            exit(1)
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')
        for tr in soup.find('tbody').find_all('tr', recursive=False):
            data['name'].append(tr.select('.views-field-title')[0].a.text.strip())
            data['protein'].append(to_zero(tr.select('.views-field-field-protein-value')[0].text.strip()))
            data['fat'].append(to_zero(tr.select('.views-field-field-fat-value')[0].text.strip()))
            data['carbohydrates'].append(to_zero(tr.select('.views-field-field-carbohydrate-value')[0].text.strip()))
            data['kcal'].append(to_zero(tr.select('.views-field-field-kcal-value')[0].text.strip()))
        print('success')

df = DataFrame(data)
with open('products.csv', mode='w+', encoding='utf8') as file:
    text = df.to_csv(index=False, line_terminator='\n', na_rep='0')
    file.write(text)
