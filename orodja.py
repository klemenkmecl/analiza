import requests
import re
import os
import csv
import time

def vrni_vsebino(datoteka):

    '''Vrne vsebino dane datoteke.'''

    with open(datoteka, 'r', encoding='utf-8') as moja_datoteka:
        return moja_datoteka.read()


def shrani(url, ime_datoteke):

    try:
        vsebina_strani = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
    else:
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            besedilo = str(vsebina_strani.text)
            datoteka.write(besedilo)
            print('Shranjeno!')

def ustvari_csv_datoteko(slovarji_restavracij):

    '''Funkcija iz slovarja ustvari csv datoteko.'''

    with open('..\\tabela.csv', 'w', encoding='utf-8') as csv_datoteka:
        naslovi = ('id', 'Ime restavracije', 'Mesto', 'Država', 'Ocena', 'Število ocen', 'Cena', 'Vrsta restavracije')
        pisec = csv.DictWriter(csv_datoteka, fieldnames=naslovi)
        pisec.writeheader()
        for slovar in slovarji_restavracij:
            pisec.writerow(slovar)

def ustvari_slovarja_mest():

    '''Funkcija najprej iz datoteke prva_stran.html pridobi seznam držav in mest v katerih se nahajajo restavracije. Najprej ustvari dva slovarja,
    v prvem vsakemu mestu pripada niz, ki je del url naslova, v drugem slovarju pa vsakemu mestu pripada država, v kateri se mesto nahaja. Nato vrne
    ta dva slovarja.'''

    vsebina_datoteke = vrni_vsebino('..\\prva_stran.html')

    regex_drzave = re.compile(r'<li class="state">\s*<div>(?P<drzava>[A-Z]+)</div>\s*<ul class="cities">(?P<mesta>.*?)</ul>\s*</li>', flags=re.DOTALL)
    regex_mesta = re.compile(r'<li><a href="/(?P<urlmesta>.*?)">(?P<mesto>.*?)</a></li>', flags=re.DOTALL)

    mesta_naslovi = {}
    mesta_drzave = {}

    for drzava in re.finditer(regex_drzave, vsebina_datoteke):
        for mesto in re.finditer(regex_mesta, drzava.group('mesta')):
            mesta_naslovi[mesto.group('mesto')] = mesto.group('urlmesta')
            mesta_drzave[mesto.group('mesto')] = drzava.group('drzava')

    return mesta_naslovi, mesta_drzave


def prenesi_html_datoteke(mesta_naslovi, mesta_drzave):

    '''Funkcija preveri, ali že obstaja mapa z imenom mesta. Če ne, jo ustvari.'''

    if not os.path.exists('..\\mesta'):
            os.mkdir('..\\mesta')

    '''Funkcija za vsako mesto iz slovarja mest ustvari mapo z imenom mesta, vanjo pa shrani pet html datotek.
    Vsaka od teh datotek vsebuje podatke o desetih restavracijah. Za vsako mesto imamo torej podatke o petdesetih
    restavracijah.'''


    for mesto in mesta_naslovi.keys():
        url_mesta = 'http://www.yelp.com/search?find_desc=Restaurants&find_loc=' + mesta_naslovi[mesto] + '&start={}&sortby=review_count'
        if not os.path.exists('..\\mesta\\' + mesto):
                os.mkdir('..\\mesta\\' + mesto)
        for i in range(1, 6):
            relativna_pot_datoteke = '..\\mesta\\' + mesto + '\\stran{}.html'.format(str(i))
            if os.path.isfile(relativna_pot_datoteke):
                print('Že shranjeno!')
                continue
            shrani(url_mesta.format(str((i - 1)*10)), relativna_pot_datoteke)
            time.sleep(0.05)

def ustvari_slovarje_restavracij(mesta_drzave):

    stevec_restavracij = 1
    slovarji_restavracij = []
    # prejšnji regex
    # regex_strani = re.compile(r'<div class="media-story">\s+<h3 class="search-result-title">\s+<span class="indexed-biz-name">(?P<stevilo>\d+)\.\s+<a class="biz-name js-analytics-click" data-analytics-label="biz-name" href=".*?" data-hovercard-id=".*?" ><span >(?P<ime>.*?)</span>.*?<i class="star-img .*?" title="(?P<zvezdice>.*?) star rating">.*?<span class="review-count rating-qualifier">\s+(?P<stevilo_ocen>\d+)\s+reviews?.*?<span class="business-attribute price-range">(?P<cena>.*?)</span>.*?<span class="category-str-list">(?P<tipi>.*?)</span>', re.DOTALL)
    regex_strani = re.compile(r'<div class="media-story">\s+<h3 class="search-result-title">\s+<span class="indexed-biz-name">(?P<stevilo>\d+)\.\s+<a class="biz-name js-analytics-click" data-analytics-label="biz-name" href=".*?" data-hovercard-id=".*?" ><span >(?P<ime>.*?)</span></a>.*?<div class=".*?" title="(?P<zvezdice>.*?) star rating">.*?<span class="review-count rating-qualifier">\s+(?P<stevilo_ocen>\d+) reviews?.*?<span class="business-attribute price-range">(?P<cena>.*?)</span>.*?<span class="category-str-list">(?P<tipi>.*?)</span>', re.DOTALL)

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
                slovarji_restavracij.append(slovar_restavracije)
                stevec_restavracij += 1

    return slovarji_restavracij