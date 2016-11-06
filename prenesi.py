import requests
import re
import os
import csv
import time
import orodja

if not os.path.isfile('..\\prva_stran.html'):
    orodja.shrani('https://www.yelp.com/locations', '..\\prva_stran.html')

orodja.prenesi_html_datoteke()

regex_strani = re.compile(r'<div class="media-story">\s+<h3 class="search-result-title">\s+<span class="indexed-biz-name">(?P<stevilo>\d+)\.\s+<a class="biz-name js-analytics-click" data-analytics-label="biz-name" href=".*?" data-hovercard-id=".*?" ><span >(?P<ime>.*?)</span>.*?<i class="star-img .*?" title="(?P<zvezdice>.*?) star rating">.*?<span class="review-count rating-qualifier">\s+(?P<stevilo_ocen>\d+)\s+reviews?.*?<span class="business-attribute price-range">(?P<cena>.*?)</span>.*?<span class="category-str-list">(?P<tipi>.*?)</span>', re.DOTALL)

stevec_restavracij = 1

slovarji_restavracij = []

for mapa in os.listdir('..\\mesta'):
    for datoteka in os.listdir('..\\mesta\\' + mapa):
        pot = '..\\mesta\\' + mapa + '\\' + datoteka
        html_strani = vrni_vsebino(pot)
        for vnos in re.finditer(regex_strani, html_strani):
            html_tipov = vnos.group('tipi')
            regex_tipov = re.compile(r'<a href=".*?">(?P<tip>.*?)</a>', re.DOTALL)
            seznam_tipov = []
            for tip in re.finditer(regex_tipov, html_tipov):
                seznam_tipov.append(tip.group('tip'))
            niz_tipov = ', '.join(seznam_tipov)
            slovar_restavracije = {}
            slovar_restavracije['id'] = str(stevec_restavracij)
            slovar_restavracije['Ime restavracije'] = vnos.group('ime')
            slovar_restavracije['Mesto'] = mapa
            slovar_restavracije['Država'] = mesta_drzave.get(mapa)
            slovar_restavracije['Ocena'] = vnos.group('zvezdice')
            slovar_restavracije['Število ocen'] = vnos.group('stevilo_ocen')
            slovar_restavracije['Cena'] = vnos.group('cena')
            slovar_restavracije['Vrsta restavracije'] = niz_tipov
            # print(vnos.group('stevilo'), vnos.group('ime'), vnos.group('zvezdice'), vnos.group('stevilo_ocen'), vnos.group('cena'), niz_tipov, str(stevcek))
            slovarji_restavracij.append(slovar_restavracije)
            stevec_restavracij += 1

'''Začasno!'''

for slovar in slovarji_restavracij:
    print(slovar)


orodja.ustvari_csv_datoteko(slovarji_restavracij)