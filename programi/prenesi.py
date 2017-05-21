import os
import orodja

'''Program prenese html datoteke s strani http://www.yelp.com.'''

if not os.path.isfile('..\\prva_stran.html'):
    orodja.shrani('http://www.yelp.com/locations', '..\\prva_stran.html')

mesta_naslovi, mesta_drzave = orodja.ustvari_slovarja_mest()

orodja.prenesi_html_datoteke(mesta_naslovi, mesta_drzave)

