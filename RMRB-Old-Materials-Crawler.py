import requests
import os
import datetime
import time
from bs4 import BeautifulSoup
import random
import re
import unicodedata

def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield b_date + day * i

def get_date_list(beginDate, endDate):
    start = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    end = datetime.datetime.strptime(endDate, "%Y-%m-%d")

    data = []
    for d in gen_dates(start, (end - start).days + 1):
        data.append(d.strftime("%Y-%m-%d"))

    return data

def generate_random_header():
    headers_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    ]
    return {"User-Agent": random.choice(headers_list)}

def save_file(content, path, filename):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
        f.write(content)

def fetch_urls(dataurl):
    headers = generate_random_header()
    r = requests.get(dataurl, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [div.find('a')['href'] for div in soup.find_all('div', class_='card mt-2')]
    return links

def crawl_and_save_articles(links, destdir, year, month, day):
    for link in links:
        headers = generate_random_header()
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        article_elements = soup.find_all('div', class_='card mt-2')

        for article in article_elements:
            article_title = article.find('h2', class_='card-title text-center text-dark bg-light p-1').text.strip()
            article_content = article.find('div', class_='card-body').get_text(separator='\n').strip()
            content = f'{article_title}\n\n{article_content}'
            path = os.path.join(destdir, year, f'{year}-{month}', f'{year}-{month}-{day}')
            filename = '{}.txt'.format(re.sub(r'\W+', '_', unicodedata.normalize('NFKD', content[:30].strip())))
            save_file(content, path, filename)

def crawl_articles(beginDate, endDate, destdir):
    data = get_date_list(beginDate, endDate)

    for date_str in data:
        year, month, day = date_str.split('-')
        dataurl = f'https://www.laoziliao.net/rmrb/{year}-{month}-{day}'
        links = fetch_urls(dataurl)
        crawl_and_save_articles(links, destdir, year, month, day)

        print(f'Articles for {date_str} have been crawled and saved.')
        time.sleep(5)

    print('All articles have been crawled and saved.')

if __name__ == '__main__':
    beginDate = 'YYYY-MM-DD'  # Replace 'YYYY-MM-DD' with the desired start date.
    endDate = 'YYYY-MM-DDD'  # Replace 'YYYY-MM-DD' with the desired start date.
    destdir = ''  # Set 'destdir' to the desired directory path where you want the files to be saved.

    crawl_articles(beginDate, endDate, destdir)
