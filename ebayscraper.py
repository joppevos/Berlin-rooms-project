import requests
from bs4 import BeautifulSoup
import sqlite3
import time


def room_scraper(conn, c):
    page = 1
    sitepage = ''
    while True:
        try:
            html = requests.get('https://www.ebay-kleinanzeigen.de/s-immobilien/berlin/anbieter:privat/'
                                'anzeige:angebote/preis:200:900/{}zimmer/k0c195l3331'
                                .format(sitepage))
            print(html)
        except:
            print('invalid request')
            break

        if f'seite:{page}' not in html.url and sitepage is not '':
            print('end of pages')
            break

        soup = BeautifulSoup(html.content, 'html.parser')
        # print(soup)
        article = soup.find_all('article', class_='aditem')
        if article == []:
            print('cannot find ads')
            break

        ads = {}
        for i in article:
            sizem = i.find('p', class_='text-module-end')
            sizem = sizem.text.replace(' ', '').split()
            # check for square and room count
            if len(sizem) == 2:
                ads['rooms'] = sizem[0]
                ads['square'] = sizem[1]
            elif sizem == []:
                ads['rooms'] = ''
                ads['square'] = ''
            elif 'Zimmer' in sizem[0]:
                ads['rooms'] = sizem[0]
                ads['square'] = ''
            else:
                ads['square'] = sizem[0]
                ads['rooms'] = ''

            ads = {k: v.replace('Zimmer', '').replace('m²', '') for k, v in ads.items()}

            priceloc = i.find('div', class_='aditem-details')
            priceloc = ((priceloc.text).replace(' ', '').replace('€', '').replace('VB', '')).split()
            ads['price'] = priceloc[0]
            ads['location'] = priceloc[2]

            c.execute("INSERT INTO rooms VALUES (:price, :location, :rooms, :square)",
                      {'price': ads['price'], 'location': ads['location'],
                       'rooms': ads['rooms'], 'square': ads['square']})
            conn.commit()
            print(ads)

        print(f'Scraping page {page}')
        time.sleep(0.3)
        page += 1

        sitepage = 'seite:{}/'.format(page)


def database():
    conn = sqlite3.connect('ebay-rooms.db')
    c = conn.cursor()
    c.execute("DROP TABLE rooms")
    c.execute("""CREATE TABLE rooms(
                price,
                location TEXT, 
                rooms,
                square 
                )""")
    return conn, c


database()
room_scraper(*database())
