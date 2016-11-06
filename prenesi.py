import requests
import re
import os
import csv
import time

test

def vrni_vsebino(datoteka):

    'Vrne vsebino dane datoteke.'

    with open(datoteka, 'r', encoding='utf-8') as moja_datoteka:
        return moja_datoteka.read()


def shrani(url, ime_datoteke):

    try:
        vsebina_strani = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
    else:
        print(vsebina_strani.encoding)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            besedilo = str(vsebina_strani.text)
            datoteka.write(besedilo)
            print('Shranjeno!')

#shrani('https://www.yelp.com/locations', 'prva_stran.html')


#regex_drzave = re.compile(r'<li class="state">\\n\s+<div>(?P<drzava>[A-Z]+)</div>\\n\s+<ul class="cities">\\n\s+(?P<mesta>.*?)\s+</ul>\\n\s+</li>\\n', flags=re.DOTALL)
#regex_mesta = re.compile(r'<li><a href="/(?P<urlmesta>.*?)">(?P<mesto>.*?)</a></li>\\n', flags=re.DOTALL)
regex_drzave = re.compile(r'<li class="state">\s*<div>(?P<drzava>[A-Z]+)</div>\s*<ul class="cities">(?P<mesta>.*?)</ul>\s*</li>', flags=re.DOTALL)
regex_mesta = re.compile(r'<li><a href="/(?P<urlmesta>.*?)">(?P<mesto>.*?)</a></li>', flags=re.DOTALL)

vsebina_datoteke = vrni_vsebino('prva_stran.html')

# for drzava in re.finditer(regex_drzave, vsebina_datoteke):
#     for mesto in re.finditer(regex_mesta, drzava.group('mesta')):
#         print(drzava.group('drzava'), mesto.group('mesto'), mesto.group('urlmesta'))

""" Ustvari dva slovarja."""

mesta_naslovi = {}
mesta_drzave = {}

for drzava in re.finditer(regex_drzave, vsebina_datoteke):
    for mesto in re.finditer(regex_mesta, drzava.group('mesta')):
        # if '%' in mesto.group('urlmesta') or '\\\\' in mesto.group('mesto') or '\\\\' in drzava.group('drzava'):
        #     pass
        # else:
        mesta_naslovi[mesto.group('mesto')] = mesto.group('urlmesta')
        mesta_drzave[mesto.group('mesto')] = drzava.group('drzava')
        # print(drzava.group('drzava'), mesto.group('mesto'), mesto.group('urlmesta'))
#
# print(mesta_naslovi)
# print(mesta_drzave)
#
# if not os.path.exists('mesta'):
#             os.mkdir('mesta')
#
# for mesto in mesta_naslovi.keys():
#     stevec = 0
#     url_mesta = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=' + mesta_naslovi[mesto] + '&sortby=review_count&start={}'
#     if not os.path.exists('mesta\\' + mesto):
#             os.mkdir('mesta\\' + mesto)
#     for _ in range(5):
#         relativna_pot_datoteke = 'mesta\\' + mesto + '\\stran{}.html'.format(str(stevec))
#         shrani(url_mesta.format(str(stevec)), relativna_pot_datoteke)
#         stevec += 10
#         time.sleep(0.05)

regex_strani = re.compile(r'<div class="media-story">\s+<h3 class="search-result-title">\s+<span class="indexed-biz-name">(?P<stevilo>\d+)\.\s+<a class="biz-name js-analytics-click" data-analytics-label="biz-name" href=".*?" data-hovercard-id=".*?" ><span >(?P<ime>.*?)</span>.*?<i class="star-img .*?" title="(?P<zvezdice>.*?) star rating">.*?<span class="review-count rating-qualifier">\s+(?P<stevilo_ocen>\d+)\s+reviews?.*?<span class="business-attribute price-range">(?P<cena>.*?)</span>.*?<span class="category-str-list">(?P<tipi>.*?)</span>', re.DOTALL)

stevec_restavracij = 1

slovarji_restavracij = []

for mapa in os.listdir('mesta'):
    for datoteka in os.listdir('mesta\\' + mapa):
        pot = 'mesta\\' + mapa + '\\' + datoteka
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

for slovar in slovarji_restavracij:
    print(slovar)


with open('tabela.csv', 'w') as csv_datoteka:
    naslovi = ('id', 'Ime restavracije', 'Mesto', 'Država', 'Ocena', 'Število ocen', 'Cena', 'Vrsta restavracije')
    pisec = csv.DictWriter(csv_datoteka, fieldnames=naslovi)
    pisec.writeheader()
    for slovar in slovarji_restavracij:
        pisec.writerow(slovar)