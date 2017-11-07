import sqlite3 as lite
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import sqlite3 as lite

url = "https://www.bytbil.com/stockholms-lan/personbil-scenic-renault-scenic-ii-2-0-16v-134hk-8668-11428948"
r = requests.get(url)
data = r.text

soup = BeautifulSoup(data, "html.parser")
price = soup.find("span", class_="car-price-details").get_text().strip()
price = price.split()[0]+price.split()[1]
print "Pris," + price

details = soup.find("div", class_="object-info-box equipment-list-equal")
for d in details.find_all('dl'):
    print list(d.children)[3].string + ',' + list(d.children)[1].string

extras = soup.find("div", class_="uk-grid uk-grid-width-medium-1-3").find_all('li')
for e in extras:
	print e.string




def fileToSqlite():
   file = open('out.txt')

   # connect to db
   db = lite.connect('bytbil.com.sqlite')

   # create a cursor
   cur = db.cursor()

   currentDate = datetime.today().strftime('%Y-%m-%d')

   for line in file:
   
      link = "https://www.bytbil.com" + line.strip()
      query = u"INSERT INTO car_links (link, date, annons_id) VALUES (\'%s\', \'%s\', \'%s\');" % (link, "2017-11-02", "n")
      try:
         cur.execute(query)
      except Exception as e:
   	     print e
   db.commit()
