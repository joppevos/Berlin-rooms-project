import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import os

def room_scraper(conn, c):
    page = 1
    sitepage = ''
    while True:
        try:
            html = requests.get('https://www.ebay-kleinanzeigen.de/s-immobilien/berlin/anbieter:privat/'
                                'anzeige:angebote/preis:200:1200/{}zimmer/k0c195l3331'
                                .format(sitepage))
            # print(html)
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

        for i in article:
            """
            search the room article for features
            locates and add to dict 'ads'
            commit dict to sqlite db
            """
            ads = {}
            title = i.find('h2', class_='text-module-begin')
            tag = title.find('a')['href']
            tag = int(os.path.basename(tag).replace('-', ''))
            # break
            ads['ID'] = tag

            priceloc = i.find('div', class_='aditem-details')
            priceloc = ((priceloc.text).replace(' ', '').replace('€', '').replace('VB', '')).split()
            ads['price'] = int(priceloc[0].replace('.', ''))
            ads['location'] = priceloc[2]

            sizem = i.find('p', class_='text-module-end')
            sizem = sizem.text.replace(' ', '').replace(',', '.').split()

            try:
                if len(sizem) == 2:
                    ads['rooms'] = int(float(sizem[0].replace('Zimmer', '')))
                    ads['square'] = int(float(sizem[1].replace('m²', '')))
                elif sizem == []:
                    ads['rooms'] = None
                    ads['square'] = None
                elif 'Zimmer' in sizem[0]:
                    ads['rooms'] = int(float(sizem[0].replace('Zimmer', '')))
                    ads['square'] = None
                else:
                    ads['square'] = int(float(sizem[0].replace('m²', '')))
                    ads['rooms'] = None
            except ValueError:
                # except mistakes in returned scrape
                continue

            db_commit(conn, c, ads)

        print(f'Scraping page {page}')
        time.sleep(0.3)
        page += 1

        sitepage = 'seite:{}/'.format(page)


def db_connect():
    conn = sqlite3.connect('ebayrooms.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE rooms(
                        price INT,
                        location TEXT,
                        rooms INT,
                        square INT,
                        ID INTEGER PRIMARY KEY
                        )""")
    except sqlite3.OperationalError:
        print('table already exists')
    return conn, c


def db_commit(conn, c, ads):
    try:
        c.execute("INSERT INTO rooms VALUES (:price, :location, :rooms, :square, :ID)",
                  {'price': (ads['price']), 'location': ads['location'],
                   'rooms': (ads['rooms']), 'square': (ads['square']), 'ID': ads['ID']})

        conn.commit()
    except sqlite3.IntegrityError:
        print('UNIQUE constraint failed')
        pass


db_connect()
room_scraper(*db_connect())
