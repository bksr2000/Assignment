from bs4 import BeautifulSoup
from requests import get
from random import choice, randint
from pandas import DataFrame
from time import sleep

delay_list = list(range(50, 150, 5))
description, ASIN, prod_description, manufacturer = [], [], [], []
product_count = randint(205, 220)
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


print('Scraping products...')

for url in links:
    sleep(choice(delay_list) / 100)

    lst = url.split('/')
    if 'dp' not in lst:
        lst = url.split('%2F')
    i = 1 + lst.index('dp')
    if len(lst[i]) == 10:
        ASIN.append(lst[i])

    try:
        webpage = get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, 'lxml')
        try:
            lis = soup.find('ul', attrs={'class': "a-unordered-list a-vertical a-spacing-mini"}).find_all('li')
            prodes = ''
            for each in lis:
                prodes += (each.text + '___')
            description.append(prodes)
        except AttributeError:
            description.append('NA')

        try:
            pd = soup.find_all('td', attrs={'class': "apm-top"})
            prodes = ''
            for each in pd:
                prodes += (each.text.strip() + '___')
            prod_description.append(prodes)
        except AttributeError:
            prod_description.append('NA')

        try:
            asin = soup.find('div', attrs={'id': "detailBullets_feature_div"}).find_all('li')
            for each in asin:
                li = each.text.split(
                    '\n                                    '
                    '\u200f\n                                        '
                    ':\n                                    '
                    '\u200e\n                                 ')
                if li[0] == ' Manufacturer':
                    manufacturer.append(li[1])
                    break
            else:
                manufacturer.append('NA')
        except AttributeError:
            manufacturer.append('NA')
    except:
        description.append('NA')
        prod_description.append('NA')
        manufacturer.append('NA')
    if len(description) is product_count:
        break

print('Done Scraping Products')
product_count = len(description)

result = DataFrame({
    'Product URL': links[0:product_count],
    # 'Producy Name': title[0:product_count],
    # 'Producy Price': price[0:product_count],
    # 'Rating': rating[0:product_count],
    # 'Number of Reviews': reviews[0:product_count],
    'Description': description,
    'ASIN': ASIN,
    'Product Description': prod_description,
    'Manufacturer': manufacturer,
})
result.to_csv("assignment_part2.csv")
