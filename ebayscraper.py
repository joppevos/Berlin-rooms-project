import requests
from bs4 import BeautifulSoup
import numpy as np
import sqlite3


def room_scraper(conn, c):
    page = 1
    while page !=3:
        site = ''
        try:
            html = requests.get('https://www.ebay-kleinanzeigen.de/s-berlin/anbieter:privat/anzeige:angebote/preis:100:650/{}zimmer/k0l3331'
                                .format(site))
            print(html)
        except:
            print('invalid request')
            break

        soup = BeautifulSoup(html.content, 'html.parser')
        # print(soup)
        article = soup.find_all('article', class_='aditem')
        if article == []:
            print('cannot find ads')
            break

        for i in article:
            features = []
            priceloc = i.find('div', class_='aditem-details')
            priceloc = ((priceloc.text).replace(' ', '').replace('€', '').replace('VB', '')).split() # remove spaces, split in list
            features.extend(priceloc)

            sizem = i.find('p', class_='text-module-end')
            sizem = sizem.text.split()
            if sizem == []:
                print('EMPTY VALUE')
                sizem.extend([None, None, None, None])
            features.extend(sizem)
            features = np.delete(features, (1, 4, 6))

            c.execute("INSERT INTO rooms VALUES (:price, :location, :rooms, :square)",
                      {'price': features[0], 'location': features[1], 'rooms': features[2], 'square': features[3]})
            conn.commit()

        page =+1
        site = 'seite:{}/'.format(page)


def database():
    conn = sqlite3.connect('ebay-rooms.db')
    c = conn.cursor()
    c.execute("DROP TABLE rooms")
    c.execute("""CREATE TABLE rooms(
                price INT,
                location INT,
                rooms INT,
                square INT
                )""")
    return conn, c

database()
room_scraper(*database())