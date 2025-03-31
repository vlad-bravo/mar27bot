import os
import sqlite3

from dotenv import load_dotenv
from lxml import html
import requests


load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')


def value_from_str(str_value: str) -> float:
    value = 0
    is_after_dp = False
    divider = 1
    for char in str_value:
        if '0' <= char <= '9':
            value = value * 10 + int(char)
            if is_after_dp:
                divider *= 10
        if char == '.' or char == ',':
            is_after_dp = True
    return value / divider

def main():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT title, url, xpath FROM parser_data'
        )
        rows = cur.fetchall()
    for title, url, xpath in rows:
        print(title)
        page = requests.get(url)
        tree = html.fromstring(page.content) 
        values = tree.xpath(xpath + '/text()')
        sum_values = 0
        count_values = 0
        for str_value in values:
            value = value_from_str(str_value)
            sum_values += value
            count_values += 1
        print(sum_values / count_values)


if __name__ == '__main__':
    main()
