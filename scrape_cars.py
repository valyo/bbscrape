#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import re
import codecs
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import sqlite3 as lite
from operator import itemgetter
from datetime import datetime, timedelta
import json
from get_cars import getCars

# from IPython.core.debugger import Tracer
# from HTMLParser import HTMLParser

# get rid of a warning message
requests.packages.urllib3.disable_warnings()



class getCarsData:

   def print_data(self,info):
      # print(",".join(['{0}'.format(k, v) for k,v in sorted(info.iteritems())]))
      print(sorted(info.iteritems()))
      # print(",".join(['{1}'.format(k, v) for k,v in sorted(info.iteritems())]))
      print(['{1}'.format(k, v) for k,v in sorted(info.iteritems())])


   # def connectDB(self):

	  #  return  lite.connect('bytbil.com.sqlite')


   def getAdPage(self, url):
      
      # make a request and get the whole page in data object
      r = requests.get(url)
      data = r.text
      soup = BeautifulSoup(data, "html.parser")
      return soup

   def getAdsLinksList(self,cur):
      
      query = "SELECT link_id,link FROM car_links WHERE annons_id = 'n';"
      cur.execute(query)
      link = list(cur.fetchall())
      return link



   def getLinksList(self, data):

      cars = list()

      # get the BeautifulSoup object
      soup = BeautifulSoup(data, "html.parser")

      # get all the car links from the page
      for h3s in soup.find_all("h3", class_="uk-text-truncate car-list-header hidden-small-and-below"):
         cars.append(h3s.find('a').get('href'))
      return cars


   def get_details(self, soup):
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
          info[key] = list(d.children)[1].string.encode('utf-8')
          # Tracer()()
      mil = ""
      for i in info['mileage']:
         match = re.search('\d',i)
         if match:
            mil+=i
      info['mileage'] = mil

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

#################################
# find the extras and process
# them
#################################
      try:
         # extras = soup.find("div", class_="uk-grid uk-grid-width-medium-1-3").find_all('li')
         extras = soup.find("div", class_="uk-width-1-1 vehicle-detail-equipment-detail").find_all('li')
      except Exception as e1:
         print("get the extras li items Exception")
         print(e1)
         try:
            extras = soup.find("ul", class_="uk-list-space equipment-list").find('li')
            # print(extras.string.split())
            extras = extras.split()

            for e in extras:
               e = e.string
               # print(e.string)
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

               match = re.search('LM-f.lgar|aluminium.*', e.string, flags=re.IGNORECASE)
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

               match = re.search('Parkering.*bak|Backkamera|Parkeringspaket|Backvarnare|Parkeringssensor.*', e.string, flags=re.IGNORECASE)
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

               if info['year'] >= 2000:
                  info['abs'] = "1"
                  info['airbag'] = "1"
                  info['fdator'] = "1"
                  info['elspeglar'] = "1"

         except Exception as e1:
           print("the alternative extras Exception")
           print(e1)


   def get_volume_hp(self,soup):
      key_list = []
      val_list = []
      try:
         all_det = soup.find("div", class_="uk-grid uk-grid-width-medium-1-3 additional-vehicle-data")
         # print(str(all_det))
         stri = " ".join(" ".join(" ".join(str(all_det.encode('utf-8')).splitlines()).split(">")).split("<"))
         # stri = " ".join(" ".join(" ".join(all_det.splitlines()).split(">")).split("<"))
         
         # print(stri)

         # match = re.search('(\d*) g CO', str(all_det.text), flags=re.IGNORECASE)
         match = re.search('(\d*) g CO', stri, flags=re.IGNORECASE)
         if match:
            info["co2"] = match.group(1)
         match = re.search('(\d*\.\d*) l/mil', stri, flags=re.IGNORECASE)
         if match:
            info["eco"] = match.group(1)
         # match = re.search('(\d*\s*\d*) cc', stri, flags=re.IGNORECASE)
         # if match:
         #    info["motor"] = match.group(1)
         match = re.search('(\d*) hk', stri, flags=re.IGNORECASE)
         if match:
            info["power"] = match.group(1)
         match = re.search('(\d{4}-\d{2}-\d{2})', stri, flags=re.IGNORECASE)
         if match:
            info["itrafik"] = match.group(0)
         keys = soup.find_all("div", class_="text-gray")
         for key in keys:
            # print(key.string)
            key_list.append(key.string)
         # print(len(key_list))
         # print(key_list)
         divs = soup.find_all("div", class_="uk-text-bold")
         for d in divs:
            # print(d)
            # print(d.string)
            val_list.append(d.string)
         # print(len(val_list))
         # print(len(val_list))
         for i in range(len(val_list)):
            # print(i)
            # print(key_list[i])
            # print(val_list[i])
            match = re.search('Modell', key_list[i], flags=re.IGNORECASE)
            if match:
               try:
                 info['spec'] = soup.find("em").string.encode('utf-8').replace(",",".")
                 # info['spec'] = val_list[i].string.encode('utf-8').strip()
               except Exception as e5:
                 print("spec Exception")
                 print(e5)
            match = re.search('F.*rg', key_list[i], flags=re.IGNORECASE)
            if match:
               # print("bla")
               info['color'] = val_list[i].string.encode('utf-8').strip()
            else:
               match = re.search('.*(Silver).*|.*(Ljusbl.).*|.*(Svart).*|.*(Vit).*|.*(Ljusgr.n).*|.*(Gr.).*|.*(Ljusbrun).*|.*(R.d).*', stri, flags=re.IGNORECASE)
               # match = re.search('\s(R.d)\s', stri, flags=re.IGNORECASE)
               if match:
                  info["color"] = match.group(1)
            match = re.search('Motorstorlek', key_list[i], flags=re.IGNORECASE)
            if match:
               info['motor'] = val_list[i].string.encode('utf-8').strip().strip()
               # print("bla")
            else:
               if "NaN" == info['motor']:
                  match = re.search('(\d.*\d) cc', stri, flags=re.IGNORECASE)
                  if match:
                     info["motor"] = match.group(1)
            match = re.search('Skattevikt', key_list[i], flags=re.IGNORECASE)
            if match:
               info['vikt'] = val_list[i].string.encode('utf-8').strip()
               # print(len(info['vikt']))
            elif len(info['vikt']) == 0:
               match = re.search('(\d.\d{3}) kg', stri, flags=re.IGNORECASE)
               if match:
                  info["vikt"] = match.group(1)

         # fix the engine displacement value   
            info['motor'] = info['motor'].replace(" cc","")
            motor = ""
            if len(info['motor']) > 8:
               info['motor'] = info['motor'][-6:]
            for i in info['motor']:
               match = re.search('\d',i)
               if match:
                  motor+=i
            info['motor'] = motor

            # fix the weigth value   
            info['vikt'] = info['vikt'].replace(" kg","")
            vikt = ""
            for i in info['vikt']:
               match = re.search('\d',i)
               if match:
                  vikt+=i
            info['vikt'] = vikt


      except Exception as e3:
         print("big get_volume_hp Exception")
         print(e3)

   def initInfo(self):
   
      #################################
      # define dic to hold the features
      #################################

      # info = {}
      info['make'] = "NaN"
      info['mileage'] = "NaN"
      info['model'] = "NaN"
      info['pris'] = "NaN"
      info['regnr'] = "NaN"
      info['year'] = "NaN"
      info['fuel_bensin'] = "0"
      info['fuel_diesel'] = "0"
      info['fuel_d_hybrid'] = "0"
      info['fuel_b_hybrid'] = "0"
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

      return info
      
 
if __name__ == "__main__":


   getCarsData = getCarsData()
   getCars = getCars()

   ### #     # ### #######
    #  ##    #  #     #
    #  # #   #  #     #
    #  #  #  #  #     #
    #  #   # #  #     #
    #  #    ##  #     #
   ### #     # ###    #

   # Bytbil.com base URL string
   # and site URL for the DB cars links
   # url = "https://www.bytbil.com/bil?Page="
   # b_link = "https://www.bytbil.com"
   # define a list to store the links
   # cars_links = list()

   info = {}
   info['make'] = "NaN"
   info['mileage'] = "NaN"
   info['model'] = "NaN"
   info['pris'] = "NaN"
   info['regnr'] = "NaN"
   info['year'] = "NaN"
   info['fuel_bensin'] = "0"
   info['fuel_diesel'] = "0"
   info['fuel_d_hybrid'] = "0"
   info['fuel_b_hybrid'] = "0"
   info['4wd'] = "0"
   info['auto'] = "0"
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


   # connect to db and create a  cursor
   db = getCars.connectDB()
   db.text_factory = str
   cur = db.cursor()

   # set current date
   currentDate = datetime.today().strftime('%Y-%m-%d')




   #     #    #    ###  #     #
   ##   ##   # #    #   ##    #
   # # # #  #   #   #   # #   #
   #  #  # #     #  #   #  #  #
   #     # #######  #   #   # #
   #     # #     #  #   #    ##
   #     # #     # ###  #     #

   # select link from car_links where annons_id = "n"
   # and get the links in a list

   #print header
   # getCarsData.initInfo()
   # print(",".join(['{0}'.format(k, v) for k,v in sorted(info.iteritems())]))

   ads = getCarsData.getAdsLinksList(cur)


   for ad in ads:

      # initialize dic holding the features
      getCarsData.initInfo()

      # ad[0] is link_id and ad[1] is the link string
      # print(ad[1])

      #get the annouce page
      soup = getCarsData.getAdPage(ad[1])
      
      # check if the car is still for sale
      match = re.search('Sidan saknas.*', soup.find("title").get_text().strip(), flags=re.IGNORECASE)
      if match:

         # the annons is removed -> continue to the next one
         # print("bla")
         continue
      else:

         # print the add link for debugging
         print(ad[1])
         
         getCarsData.get_details(soup)
         getCarsData.get_volume_hp(soup)
         # getCarsData.print_data(info)
         if info['color'] == None:
            info['color'] = "NaN"
         # for k,v in info.iteritems():
         #    v = v.decode("utf-8")
         #    print(type(v))
         #    print(v)

         query = "INSERT INTO cars_data (annons_id,awd,abs,airbag,alufalg,antisladd,antispinn,auto,bluetooth,c_las,co2,color,dimljus,dragkrok,eco,elhissar,elspeglar,farthallare,fdator,fuel_b_hybrid,fuel_bensin,fuel_d_hybrid,fuel_diesel,gps,itrafik,keyless,klima,laddhybrid,larm,ledheadl,lucka,make,mileage,model,motor,motorv,muggh,multifunktionsratt,parkassist,power,pris,rails,rattv,regnr,regnsensor,servo,skin,spec,startstop,stolminne,stolv_fram,svensks,vikt,vinterd_d,vinterd_fr,xenon,year,ytempm) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"

         try:

            cur.execute(query, ([ad[0]] + ['{1}'.format(k, v) for k,v in sorted(info.iteritems())]))
            db.commit()
            # print(ad[1])
         except Exception as e:
            print("INSERT query")
            print(e)
            # print link
            # stop = True
         if cur.rowcount == 1:
            query1 = "UPDATE car_links SET annons_id = '%s' WHERE link_id = '%s';" % ("y",ad[0])
            try:
               cur.execute(query1)
               db.commit()
            except Exception as e10:
               print(ad[0])
               print(e10)

   #    make record in car_data table
   



