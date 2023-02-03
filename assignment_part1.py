from bs4 import BeautifulSoup
from requests import get
from random import choice
from pandas import DataFrame
from time import sleep

delay_list = list(range(50, 150, 5))

url_first = 'https://www.amazon.in/s?k=bags&page='  # first half of common url
url_last = '&crid=2M096C61O4MLT&qid=1675333645&sprefix=ba%2Caps%2C283&ref=sr_pg_1'  # second half of the common url
prefix = 'https://www.amazon.in/'  # prefix for the product urls

links, title, price, rating, reviews = [], [], [], [], []
HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
print('Scraping...')
page = 1
while page < 21:  # scrapes from page 1 to 20(change as per need
    url = url_first + str(page) + url_last

    sleep(choice(delay_list) / 100)
    try:
        webpage = get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, 'lxml')
        products = soup.find_all('div', attrs={'class': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right'})
        for i in products:
            try:
                links.append(prefix+i.find('a', attrs={'class': "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}).get('href'))
            except AttributeError:
                links.append('NA')
            try:
                title.append(i.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}).text)
            except AttributeError:
                title.append('NA')
            try:
                price.append(i.find('span', attrs={'class': "a-offscreen"}).text)
            except AttributeError:
                price.append('NA')
            try:
                rating.append(i.find('div', attrs={'class': "a-row a-size-small"}).text[:3])
            except AttributeError:
                rating.append('NA')
            try:
                reviews.append(i.find('span', attrs={'class': "a-size-base s-underline-text"}).text)
            except AttributeError:
                reviews.append('NA')
        page += 1
    except:
        pass

print("Done Scraping")
result = DataFrame({
    'Product URL': links,
    'Producy Name': title,
    'Producy Price': price,
    'Rating': rating,
    'Number of Reviews': reviews,
})
result.to_csv("assignment_part1_only.csv")  # result to csv file storage
