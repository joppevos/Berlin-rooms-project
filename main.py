import requests
from bs4 import BeautifulSoup
import re
import shutil
import os


#TODO IF IMAGES ARE UP, GO TO NEXT PAGE, COMBINE TITLE AND PRICE, PLACE NAMES IN SET

def start():
    # get room links
    try:
        html = requests.get('https://www.ebay-kleinanzeigen.de/s-prenzlauer-berg/zimmer/k0l3488')
    except:
        print('invalid request')
    soup = BeautifulSoup(html.content, 'html.parser')
    for link in soup.find_all('a', href=re.compile('/s-anzeige/')):
        page = link.attrs['href']
        imagescrape(page)

def imagescrape(page):
    # get and save images
    html = requests.get('https://www.ebay-kleinanzeigen.de{}'.format(page))
    soup = BeautifulSoup(html.content, 'html.parser')
    div = soup.find('div', class_='ad-image')
    if div is not None:
        imageurl = div.img['src']
        print(imageurl)
        img = requests.get(imageurl, stream=True)
        name, ext = os.path.split(page)
        print(ext)
        with open('C:\\Users\\Joppe\\Desktop\\imagestest\\{}.jpg'.format(ext), 'wb') as f:
            shutil.copyfileobj(img.raw, f)


start()