from __future__ import print_function
import sqlite3 as lite
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import sqlite3 as lite
import re
import sys

from IPython.core.debugger import Tracer


#################################
# define dic to hold the features
#################################

info = {}
info['abs'] = "0"
info['klima'] = "0"
info['dragkrok'] = "0"
info['elhissar'] = "0"
info['elspeglar'] = "0"
info['farthallare'] = "0"
info['c-las'] = "0"
info['fdator'] = "0"
info['alufalg'] = "0"
info['multifunktionsratt'] = "0"
info['servo'] = "0"
info['stolv-fram'] = "0"
info['svensks'] = "0"
info['ytempm'] = "0"
info['muggh'] = "0"
info['dimljus'] = "0"
info['rattv'] = "0"
info['ledheadl'] = "0"
info['skin'] = "0"
info['lucka'] = "0"
info['parkassist'] = "0"
info['startstop'] = "0"
info['stolminne'] = "0"
info['bluetooth'] = "0"
info['larm'] = "0"
info['motorv'] = "0"
info['rails'] = "0"
info['vinterd-fr'] = "0"
info['vinterd-d'] = "0"
info['antisladd'] = "0"
info['antispinn'] = "0"
info['regnsensor'] = "0"
info['xenon'] = "0"
info['airbag'] = "0"
info['gps'] = "0"
info['keyless'] = "0"
info['laddhybrid'] = "0"
info['spec'] = "NaN"
info['itrafik'] = "NaN"
info['color'] = "NaN"
info['motor'] = "NaN"
info['power'] = "NaN"
info['co2'] = "NaN"
info['eco'] = "NaN"
info['vikt'] = "NaN"



#################################
# scrape tha page
#################################

def get_page(url):
   # url = sys.argv[1]
   # url = "https://www.bytbil.com/ostergotlands-lan/personbil-435-d-gran-coupe-m-sport-xdrive-6577-11441064"
   r = requests.get(url)
   data = r.text
   soup = BeautifulSoup(data, "html.parser")
   return soup


#################################
# find price
#################################

def get_details(soup):
   price = soup.find("span", class_="car-price-details").get_text().strip()
   price = price.split()[0]+price.split()[1]
   # print "Pris," + price
   info['pris'] = price
   # Tracer()()
#################################
# find the main details
#################################
   details = soup.find("div", class_="object-info-box equipment-list-equal")
   for d in details.find_all('dl'):
       # print list(d.children)[3].string + ',' + list(d.children)[1].string
       match = re.search('M.rke', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'make'

       match = re.search('Modell', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'model'

       match = re.search('.rsmodell', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'year'

       match = re.search('Miltal', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'mileage'

       match = re.search('Drivmedel', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'fuel'

       match = re.search('V.xell.da', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'auto'

       match = re.search('Drivhjul', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = '4wd'

       match = re.search('Regnr', list(d.children)[3].string, flags=re.IGNORECASE)
       if match:
          key = 'regnr'

       # info[list(d.children)[3].string] = list(d.children)[1].string
       info[key] = list(d.children)[1].string
       # Tracer()()
   if len(info['mileage'].split()) > 1:
      info['mileage'] = info['mileage'].split()[0] + info['mileage'].split()[1]

   if info['auto'] == 'Automatisk':
      info['auto'] = "1"
   else:
      info['auto'] = "0"

   if info['fuel'] == 'Bensin':
      info['fuel_bensin'] = "1"
      info['fuel_diesel'] = "0"
      info['fuel_d_hybrid'] = "0"
      info['fuel_b_hybrid'] = "0"
   elif info['fuel'] == 'Diesel':
      info['fuel_bensin'] = "0"
      info['fuel_diesel'] = "1"
      info['fuel_d_hybrid'] = "0"
      info['fuel_b_hybrid'] = "0"
   elif info['fuel'] == 'Hybrid el/diesel':
      info['fuel_bensin'] = "0"
      info['fuel_diesel'] = "0"
      info['fuel_d_hybrid'] = "1"
      info['fuel_b_hybrid'] = "0"
   elif info['fuel'] == 'Hybrid el/bensin':
      info['fuel_bensin'] = "0"
      info['fuel_diesel'] = "0"
      info['fuel_d_hybrid'] = "0"
      info['fuel_b_hybrid'] = "1"

   del info['fuel']

   if info['4wd'] == "4WD":
      info['4wd'] = "1"
   else:
      info['4wd'] = "0"

   # Tracer()()

#################################
# find the extras and process
# them
#################################
   try:
      extras = soup.find("div", class_="uk-grid uk-grid-width-medium-1-3").find_all('li')
   except Exception as e:
      # e
      try:
         extras = soup.find("ul", class_="uk-list-space equipment-list").find('li')
         # print(extras.string.split())
         extras = extras.split()
      except Exception as e1:
        e
        # print(e1) 
   # extras = soup.find("div", class_="uk-grid uk-grid-width-medium-1-3").find_all('li')
   # print len(extras)
   for e in extras:
      e = e.string
      # print e.string
      match = re.search('abs', e.string, flags=re.IGNORECASE)
      if match:
         info['abs'] = "1"

      match = re.search('Klimatanl|AC', e.string, flags=re.IGNORECASE)
      if match:
         info['klima'] = "1"

      match = re.search('Dragkrok', e.string, flags=re.IGNORECASE)
      if match:
         info['dragkrok'] = "1"

      match = re.search('Elhissar', e.string, flags=re.IGNORECASE)
      if match:
         info['elhissar'] = "1"

      match = re.search('Elspeglar', e.string, flags=re.IGNORECASE)
      if match:
         info['elspeglar'] = "1"

      match = re.search('Farth.llare', e.string, flags=re.IGNORECASE)
      if match:
         info['farthallare'] = "1"

      match = re.search('c-l.s', e.string, flags=re.IGNORECASE)
      if match:
         info['c-las'] = "1"

      match = re.search('F.rddator', e.string, flags=re.IGNORECASE)
      if match:
         info['fdator'] = "1"

      match = re.search('LM-f.lgar', e.string, flags=re.IGNORECASE)
      if match:
         info['alufalg'] = "1"

      match = re.search('Multifunktionsratt', e.string, flags=re.IGNORECASE)
      if match:
         info['multifunktionsratt'] = "1"

      match = re.search('Servostyrning|servo.*', e.string, flags=re.IGNORECASE)
      if match:
         info['servo'] = "1"

      match = re.search('Stolv.rme.*fram|Eluppv.rmda stolar fram', e.string, flags=re.IGNORECASE)
      if match:
         info['stolv-fram'] = "1"

      match = re.search('Svensks.ld', e.string, flags=re.IGNORECASE)
      if match:
         info['svensks'] = "1"

      match = re.search('Yttertemperaturm.tare', e.string, flags=re.IGNORECASE)
      if match:
         info['ytempm'] = "1"

      match = re.search('Muggh.llare', e.string, flags=re.IGNORECASE)
      if match:
         info['muggh'] = "1"

      match = re.search('Spoilerljus|dimljus', e.string, flags=re.IGNORECASE)
      if match:
         info['dimljus'] = "1"

      match = re.search('rattv.rme|Eluppv.rmd ratt', e.string, flags=re.IGNORECASE)
      if match:
         info['rattv'] = "1"

      match = re.search('Led.str.*lkastare', e.string, flags=re.IGNORECASE)
      if match:
         info['ledheadl'] = "1"

      match = re.search('l.der|skin', e.string, flags=re.IGNORECASE)
      if match:
         info['skin'] = "1"

      match = re.search('glas*taklucka', e.string, flags=re.IGNORECASE)
      if match:
         info['lucka'] = "1"

      match = re.search('Parkering.*bak|Backkamera|Parkeringspaket|Backvarnare', e.string, flags=re.IGNORECASE)
      if match:
         info['parkassist'] = "1"

      match = re.search('Start.*Stop.*funktion', e.string, flags=re.IGNORECASE)
      if match:
         info['startstop'] = "1"

      match = re.search('.*stol.*minne.*', e.string, flags=re.IGNORECASE)
      if match:
         info['stolminne'] = "1"

      match = re.search('Bluetooth', e.string, flags=re.IGNORECASE)
      if match:
         info['bluetooth'] = "1"

      match = re.search('Larm', e.string, flags=re.IGNORECASE)
      if match:
         info['larm'] = "1"

      match = re.search('Motorv.rmare', e.string, flags=re.IGNORECASE)
      if match:
         info['motorv'] = "1"

      match = re.search('Rails', e.string, flags=re.IGNORECASE)
      if match:
         info['rails'] = "1"

      match = re.search('Vinterhjul.*friktion', e.string, flags=re.IGNORECASE)
      if match:
         info['vinterd-fr'] = "1"

      match = re.search('Vinterhjul.*dub.*|Vinterhjul', e.string, flags=re.IGNORECASE)
      if match:
   	     if not info['vinterd-fr'] == "1":
   	  	    info['vinterd-d'] = "1"

      match = re.search('Antisladd', e.string, flags=re.IGNORECASE)
      if match:
         info['antisladd'] = "1"

      match = re.search('Antispinn', e.string, flags=re.IGNORECASE)
      if match:
         info['antispinn'] = "1"

      match = re.search('Regnsensor', e.string, flags=re.IGNORECASE)
      if match:
         info['regnsensor'] = "1"

      match = re.search('Xenon.*', e.string, flags=re.IGNORECASE)
      if match:
         info['xenon'] = "1"

      match = re.search('Airbag', e.string, flags=re.IGNORECASE)
      if match:
         info['airbag'] = "1"

      match = re.search('Navigator|GPS|navi', e.string, flags=re.IGNORECASE)
      if match:
         info['gps'] = "1"

      match = re.search('keyless', e.string, flags=re.IGNORECASE)
      if match:
         info['keyless'] = "1"

      match = re.search('Laddhybrid', e.string, flags=re.IGNORECASE)
      if match:
         info['laddhybrid'] = "1"
      # Tracer()()
   return info

#################################
# print the values on one line
# comma separated
#################################

def print_data(info):
   # print(",".join(['{0}'.format(k, v) for k,v in sorted(info.iteritems())]))
   print(",".join(['{1}'.format(k, v) for k,v in sorted(info.iteritems())]))


def get_volume_hp(soup):
   key_list = []
   val_list = []
   try:
      all_det = soup.find("div", class_="uk-grid uk-grid-width-medium-1-3 additional-vehicle-data")
      # print(str(all_det))
      stri = " ".join(" ".join(" ".join(str(all_det.encode('utf-8')).splitlines()).split(">")).split("<"))
      # stri = " ".join(" ".join(" ".join(all_det.splitlines()).split(">")).split("<"))
      print(stri)
      # match = re.search('(\d*) g CO', str(all_det.text), flags=re.IGNORECASE)
      match = re.search('(\d*) g CO', stri, flags=re.IGNORECASE)
      if match:
         info["co2"] = match.group(1)
      match = re.search('(\d*\.\d*) l/mil', stri, flags=re.IGNORECASE)
      if match:
         info["eco"] = match.group(1)
      match = re.search('(\d*\s*\d*) cc', stri, flags=re.IGNORECASE)
      if match:
         info["motor"] = match.group(1)
      match = re.search('(\d*) hk', stri, flags=re.IGNORECASE)
      if match:
         info["power"] = match.group(1)
      match = re.search('(\d{4}-\d{2}-\d{2})', stri, flags=re.IGNORECASE)
      if match:
         info["itrafik"] = match.group(0)
      keys = soup.find_all("div", class_="text-gray")
      for key in keys:
         key_list.append(key.string)
      print(len(key_list))
      divs = soup.find_all("div", class_="uk-text-bold")
      for d in divs:
         val_list.append(d.string)
      print(len(val_list))
      for i in range(len(val_list)):
         print(key_list[i])
         match = re.search('Modell', key_list[i], flags=re.IGNORECASE)
         if match:
            info['spec'] = soup.find("em").string.replace(",",".")
         # match = re.search('I trafik', key_list[i], flags=re.IGNORECASE)
         # if match:
         #    info['itrafik'] = val_list[i].string.encode('utf-8').strip()
         match = re.search('F.*rg', key_list[i], flags=re.IGNORECASE)
         if match:
            print("bla")
            info['color'] = val_list[i].string.encode('utf-8').strip()
         else:
            # match = re.search('>(Svart)<|>(Vit)<|>(Ljusgr.n)<|>(Gr.)<|>(Ljusbrun)<| (R.d) ', stri, flags=re.IGNORECASE)
            match = re.search('\s(R.d)\s', stri, flags=re.IGNORECASE)
            if match:
               info["color"] = match.group(1)
         # match = re.search('Motorstorlek', key_list[i], flags=re.IGNORECASE)
         # if match:
         #    info['motor'] = val_list[i].string.encode('utf-8').strip()
         # match = re.search('Motoreffekt', key_list[i], flags=re.IGNORECASE)
         # if match:
         #    info['power'] = val_list[i].string.encode('utf-8').strip()
         # match = re.search('Koldioxidutsl.pp', key_list[i], flags=re.IGNORECASE)
         # if match:
         #    m = re.search('(\d*) g CO', str(val_list[i]))
         #    info['co2'] = m.group(1)
         # match = re.search('Br.nslef.rbrukning', key_list[i], flags=re.IGNORECASE)
         # if match:
         #    info['eco'] = val_list[i].string.encode('utf-8').strip()
         match = re.search('Skattevikt', key_list[i], flags=re.IGNORECASE)
         if match:
            info['vikt'] = val_list[i].string.encode('utf-8').strip()
         else:
            match = re.search('(\d.\d{3}) kg', stri, flags=re.IGNORECASE)
            if match:
               info["vikt"] = match.group(1)
   except Exception as e3:
      e3



soup = get_page(sys.argv[1])
# print(soup)

details = get_details(soup)
get_volume_hp(soup)
print_data(info)





#########################################
# code for printing out the keys 
# as a comma separted string in one line
# print(",".join(['{0}'.format(k, v) for k,v in sorted(info.iteritems())]))
# for k in keys:
#    print(k, sep=',', end=",")
#########################################


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
   	     print(e)
   db.commit()
