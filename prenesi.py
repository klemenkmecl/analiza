import os
import orodja

if not os.path.isfile('..\\prva_stran.html'):
    orodja.shrani('https://www.yelp.com/locations', '..\\prva_stran.html')

mesta_naslovi, mesta_drzave = orodja.ustvari_slovarja_mest()

orodja.prenesi_html_datoteke(mesta_naslovi, mesta_drzave)

slovarji_restavracij = orodja.ustvari_slovarje_restavracij(mesta_drzave)

'''Začasno!'''

for slovar in slovarji_restavracij:
    print(slovar)


orodja.ustvari_csv_datoteko(slovarji_restavracij)