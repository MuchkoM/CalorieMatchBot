import asyncio
import functools
from collections import defaultdict
from typing import Optional

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pandas import DataFrame
import datetime


def to_zero(value):
    if not value:
        return '0'
    else:
        return value


async def parse_page(text: str):
    soup = BeautifulSoup(text, 'html.parser')
    partial_data = defaultdict(list)
    for tr in soup.find('tbody').find_all('tr', recursive=False):
        partial_data['name'].append(tr.select('.views-field-title')[0].a.text.strip())
        partial_data['protein'].append(to_zero(tr.select('.views-field-field-protein-value')[0].text.strip()))
        partial_data['fat'].append(to_zero(tr.select('.views-field-field-fat-value')[0].text.strip()))
        partial_data['carbohydrates'].append(
            to_zero(tr.select('.views-field-field-carbohydrate-value')[0].text.strip()))
        partial_data['kcal'].append(to_zero(tr.select('.views-field-field-kcal-value')[0].text.strip()))

    return partial_data


def semaphore(max_task):
    sem = asyncio.Semaphore(max_task)

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            async with sem:
                return await func(*args, **kwargs)

        return wrapped

    return wrapper


# this server can hold only 20 parallels connections
@semaphore(20)
async def get_data(session: ClientSession, i: int) -> Optional[defaultdict]:
    async with session.get('https://calorizator.ru/product/all?page={}'.format(i)) as resp:
        if resp.status == 200:
            return await parse_page(await resp.text())
        else:
            print(resp.reason, i)
            return None


async def main():
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(get_data(session, i)) for i in range(75)]
        result = await asyncio.gather(*tasks)
    data = defaultdict(list)

    for part_data in result:
        if not part_data:
            continue
        for k, v in part_data.items():
            data[k].extend(v)

    df = DataFrame(data)
    df.to_csv('products.csv', index=False, line_terminator='\n', na_rep='0')
    print(df.count())


if __name__ == '__main__':
    print('Task is started at', datetime.datetime.now())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print('Task is finished at', datetime.datetime.now())
