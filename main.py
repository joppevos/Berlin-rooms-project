import requests
from bs4 import BeautifulSoup
import re
import shutil
import os


#TODO IF IMAGES ARE UP, GO TO NEXT PAGE, COMBINE TITLE AND PRICE, PLACE NAMES IN SET
# TODO: FIX WHILE LOOP FOR END OF PAGE
def start():
    # get room links
    nextpage = ''
    pagenum = 1
    while pagenum != 9:
        print(pagenum)
        try:
            html = requests.get('https://www.ebay-kleinanzeigen.de/s-prenzlauer-berg/{}zimmer/k0l3488'.format(nextpage))
        except:
            print('invalid request')
            break
        soup = BeautifulSoup(html.content, 'html.parser')
        x = soup.find_all('a', href=re.compile('/s-anzeige/'))
        if x:
            for link in x:
                page = link.attrs['href']
                imagescrape(page, pagenum)

            print(f'nextpage is: {nextpage}')
            pagenum += 1
            nextpage = 'seite:{}/'.format(pagenum)
        else:
            print('empty soup')
            break


def imagescrape(page, pagenum):
    # get and save images
    html = requests.get('https://www.ebay-kleinanzeigen.de{}'.format(page))
    soup = BeautifulSoup(html.content, 'html.parser')
    div = soup.find('div', class_='ad-image')
    if div is not None:
        imageurl = div.img['src']
        img = requests.get(imageurl, stream=True)
        name, ext = os.path.split(page)
        with open('C:\\Users\\Joppe\\Desktop\\imagestest\\{}.jpg'.format(ext), 'wb') as f:
            shutil.copyfileobj(img.raw, f)
            print(f'downloaded image {name}')
    else:
        return


start()
