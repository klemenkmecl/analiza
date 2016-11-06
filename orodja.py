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


def prenesi_html_datoteke():

    '''Funkcija najprej iz datoteke prva_stran.html pridobi seznam držav in mest v katerih se nahajajo restavracije. Najprej ustvari dva slovarja,
    v prvem vsakemu mestu pripada niz, ki je del url naslova, v drugem slovarju pa vsakemu mestu pripada država, v kateri se mesto nahaja.'''

    vsebina_datoteke = vrni_vsebino('..\\prva_stran.html')

    regex_drzave = re.compile(r'<li class="state">\s*<div>(?P<drzava>[A-Z]+)</div>\s*<ul class="cities">(?P<mesta>.*?)</ul>\s*</li>', flags=re.DOTALL)
    regex_mesta = re.compile(r'<li><a href="/(?P<urlmesta>.*?)">(?P<mesto>.*?)</a></li>', flags=re.DOTALL)

    mesta_naslovi = {}
    mesta_drzave = {}

    for drzava in re.finditer(regex_drzave, vsebina_datoteke):
        for mesto in re.finditer(regex_mesta, drzava.group('mesta')):
            mesta_naslovi[mesto.group('mesto')] = mesto.group('urlmesta')
            mesta_drzave[mesto.group('mesto')] = drzava.group('drzava')

    '''Funkcija preveri, ali že obstaja mapa z imenom mesta. Če ne, jo ustvari.'''

    if not os.path.exists('..\\mesta'):
            os.mkdir('..\\mesta')

    '''Funkcija za vsako mesto iz slovarja mest ustvari mapo z imenom mesta, vanjo pa shrani pet html datotek.
    Vsaka od teh datotek vsebuje podatke o desetih restavracijah. Za vsako mesto imamo torej podatke o petdesetih
    restavracijah.'''


    for mesto in mesta_naslovi.keys():
        url_mesta = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=' + mesta_naslovi[mesto] + '&sortby=review_count&start={}'
        if not os.path.exists('..\\mesta\\' + mesto):
                os.mkdir('..\\mesta\\' + mesto)
        for i in range(1, 6):
            relativna_pot_datoteke = '..\\mesta\\' + mesto + '\\stran{}.html'.format(str(i))
            if os.path.isfile(relativna_pot_datoteke):
                print('Že shranjeno!')
                continue
            shrani(url_mesta.format(str((i - 1)*10)), relativna_pot_datoteke)
            time.sleep(0.05)