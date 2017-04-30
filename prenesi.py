import os
import orodja

if not os.path.isfile('..\\prva_stran.html'):
    orodja.shrani('http://www.yelp.com/locations', '..\\prva_stran.html')

mesta_naslovi, mesta_drzave = orodja.ustvari_slovarja_mest()

# orodja.prenesi_html_datoteke(mesta_naslovi, mesta_drzave)

slovarji_restavracij = orodja.ustvari_slovarje_restavracij(mesta_drzave)

'''Začasno!'''


# seznam_tipov = []
slovar_tipov = {}
seznam_slovarjev_filmi_tipi = []


stevec_kljucev = 0
for slovar in slovarji_restavracij:
    for niz in slovar['Vrsta restavracije'].split(','):
        tip = niz.strip()
        # if not tip in seznam_tipov:
        #     seznam_tipov.append(tip)
        if not tip in slovar_tipov.values():
            slovar_tipov[stevec_kljucev + 1]=tip
            stevec_kljucev += 1
        slovar_filmi_tipi = {}
        slovar_filmi_tipi['id']=slovar['id']
        slovar_filmi_tipi['Vrsta restavracije']=tip
        seznam_slovarjev_filmi_tipi.append(slovar_filmi_tipi)
    slovar.pop('Vrsta restavracije')

# print(seznam_tipov)
print(slovar_tipov)

for slovar in seznam_slovarjev_filmi_tipi:
    print(slovar)

for slovar in slovarji_restavracij:
    print(slovar)

naslovi_restavracije = ('id', 'Ime restavracije', 'Mesto', 'Država', 'Ocena', 'Število ocen', 'Cena')
naslovi_tipi = ('id', 'Vrsta restavracije')
orodja.ustvari_csv_datoteko(slovarji_restavracij, 'tabela_restavracij', naslovi_restavracije)
orodja.ustvari_csv_datoteko(seznam_slovarjev_filmi_tipi, 'tabela_tipov', naslovi_tipi)
