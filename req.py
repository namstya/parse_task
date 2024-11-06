import requests
from bs4 import BeautifulSoup as bs
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
base_url = 'https://quotes.toscrape.com/'

def parse(soup, data):
    div = soup.find_all('div', class_='quote')

    for row in div:
        quote = row.find('span', class_='text').text
        author = row.find('small', class_= 'author').text
        tags_all = row.find('div', class_='tags').find_all('a', class_='tag')
        
        tags = []
        for tag in tags_all:
            tags.append(tag.text)

        data.append({
                'quote': quote,
                'author': author,
                'tags': tags,
            })
        
request = requests.get(base_url, headers=headers)
soup = bs(request.text, 'lxml')

data = []
parse(soup, data)

next_page = soup.find('li', class_='next')
while next_page is not None:
    next_page_url = next_page.find('a', href=True)['href']
    request = requests.get(base_url + next_page_url, headers=headers)
    soup = bs(request.text, 'lxml')

    parse(soup, data)

    next_page = soup.find('li', class_='next')

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

