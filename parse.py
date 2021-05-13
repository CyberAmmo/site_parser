import requests
import csv
import os

from bs4 import BeautifulSoup

# URL = 'https://auto.ria.com/newauto/marka-lexus/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Accept': '*/*'
}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    res = requests.get(url, headers=HEADERS, params=params)
    
    return res


def get_pages_num(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('span', class_='mhide')
    if pages:
        return int(pages[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')
    
    cars = []
    for item in items:
        hrn_price = item.find('span', class_='size16')
        if hrn_price:
            hrn_price = hrn_price.get_text(strip=True)
        else:
            hrn_price = 'Цену уточняйте'
        cars.append({
            'title': item.find('span', class_='link').get_text(strip=True),
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'hrn_price': hrn_price,
            'city': item.find('span', class_='region').get_text(strip=True),
        })
    return cars


def save_csv(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Цена в $', 'Цена в грн', 'Город нахождения'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['hrn_price'], item['city']])


def parse():
    URL = input('Введите URL: ').strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_num = get_pages_num(html.text)
        for page in range(1, pages_num + 1):
            print(f'Обработка страницы {page} из {pages_num}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_csv(cars, FILE)
        print(f'Получено {len(cars)} авто')
        # os.startfile(FILE)
    else:
        print('Error')


parse()