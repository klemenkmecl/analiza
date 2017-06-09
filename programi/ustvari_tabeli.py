import os
import orodja

'''Program ustvari dve csv datoteki, v kateri shrani tabelo restavracij in tabelo tipov.'''

_, mesta_drzave = orodja.ustvari_slovarja_mest()

slovarji_restavracij, slovarji_tipov = orodja.ustvari_seznama_restavracij_in_tipov(mesta_drzave)

naslovi_restavracije = ('id', 'Ime restavracije', 'Mesto', 'Država', 'Ocena', 'Število ocen', 'Cena')
naslovi_tipi = ('id', 'Tip restavracije')
if not os.path.isfile('..\\tabela_restavracij.csv'):
    orodja.ustvari_csv_datoteko(slovarji_restavracij, 'tabela_restavracij', naslovi_restavracije)
if not os.path.isfile('..\\tabela_tipov.csv'):
    orodja.ustvari_csv_datoteko(slovarji_tipov, 'tabela_tipov', naslovi_tipi)