# Парсинг сайта Quotes to Scrape
Данные были полученые с сайта [Quotes to Scrape](https://quotes.toscrape.com/). Были вытащены цитаты, авторы и теги и оформлены в формате JSON файла.

## Что использовать для сбора информации
Если открыть средства разработчика веб-страницы и посмотреть вкладку сеть, то можно заметить, что при сайт не выполняет никаких запросов. Это значит, что страница является статической. 

Поскольку сайт имеет не динамичсекие данные, значит библиотека Selenium в данном случае не имеет смысла, т.к. она только понизит производительность. Поэтому для извлечения данных использовались библиотеки Requests и BeautifulSoup.

## Этапы работы
1. Задаем заголовки (нужны для того, чтобы сайт не решил, что вы бот и не заблокировал доступ) и полный url сайта.
```python
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
  base_url = 'https://quotes.toscrape.com/'
```
2. Для того, чтобы обратиться к сайту нужно создать GET заопрос и с помощью BeautifulSoup получить объект из которого легко извлекать данные.
```python
  request = requests.get(base_url, headers=headers)
  soup = bs(request.text, 'lxml')
```
3. Далее пишем функцию для извлечения данных со странички. С помощью средств разработчика можно узнать в каких элементах HTML содержаться нужные нам данные. Находим их и извлекаем методом find с преобразованием в текст. Добавляем полученные данные в словарь и массив.
```python
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
```
4. Поскольку страниц у нас несколько, то нужно найти на них ссылки и извлечь данные с каждой из них. В коде страницы можно найти, где хранится ссылка на следующую страницу. Поэтому пока ссылка на следующую станицу не пустая, мы ее берем и привычным методом GET и BeautifulSoup получаем объект, с которого извлекаем данные созданной функцие парсинга.
```python
  next_page = soup.find('li', class_='next')
  while next_page is not None:
    next_page_url = next_page.find('a', href=True)['href']
    request = requests.get(base_url + next_page_url, headers=headers)
    soup = bs(request.text, 'lxml')

    parse(soup, data)

    next_page = soup.find('li', class_='next')
```
5. Записываем полученные данные в JSON файл.
```python
  with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
```
