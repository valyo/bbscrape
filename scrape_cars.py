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

# from IPython.core.debugger import Tracer
# from HTMLParser import HTMLParser

# get rid of a warning message
requests.packages.urllib3.disable_warnings()



class getCarsData:

   def print_data(self,info):
      # print(",".join(['{0}'.format(k, v) for k,v in sorted(info.iteritems())]))
      print(",".join(['{1}'.format(k, v) for k,v in sorted(info.iteritems())]))


   def connectDB(self):

	   return  lite.connect('bytbil.com.sqlite')


   def getAdPage(self, url):
      
      # make a request and get the whole page in data object
      r = requests.get(url)
      data = r.text
      soup = BeautifulSoup(data, "html.parser")
      return soup

   def getAdsLinksList(self,cur):
      
      # link_id = list()
      # link = list()
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
         # print(len(key_list))
         divs = soup.find_all("div", class_="uk-text-bold")
         for d in divs:
            val_list.append(d.string)
         # print(len(val_list))
         for i in range(len(val_list)):
            # print(key_list[i])
            # print(val_list[i])
            match = re.search('Modell', key_list[i], flags=re.IGNORECASE)
            if match:
               info['spec'] = soup.find("em").string.replace(",",".")
            # match = re.search('I trafik', key_list[i], flags=re.IGNORECASE)
            # if match:
            #    info['itrafik'] = val_list[i].string.encode('utf-8').strip()
            match = re.search('F.*rg', key_list[i], flags=re.IGNORECASE)
            if match:
               # print("bla")
               info['color'] = val_list[i].string.encode('utf-8').strip()
            else:
               match = re.search('.*(Ljusbl.).*|.*(Svart).*|.*(Vit).*|.*(Ljusgr.n).*|.*(Gr.).*|.*(Ljusbrun).*|.*(R.d).*', stri, flags=re.IGNORECASE)
               # match = re.search('\s(R.d)\s', stri, flags=re.IGNORECASE)
               if match:
                  info["color"] = match.group(1)
            match = re.search('Motorstorlek', key_list[i], flags=re.IGNORECASE)
            if match:
               info['motor'] = val_list[i].string.encode('utf-8').strip()
               # print("bla")
            else:
               if "NaN" == info['motor']:
                  match = re.search('(\d.*\d) cc', stri, flags=re.IGNORECASE)
                  if match:
                     info["motor"] = match.group(1)
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

         # fix the engine displacement value   
         info['motor'] = info['motor'].replace(" cc","")
         motor = ""
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
         e3

 
if __name__ == "__main__":


   getCarsData = getCarsData()

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


   # define a counter; set it to 1
   # c = 1

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


   # connect to db and create a  cursor
   db = getCarsData.connectDB()
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
   ads = getCarsData.getAdsLinksList(cur)


   for ad in ads:

      # ad[0] is link_id and ad[1] is the link string
      # print ad[1]

      #get the annouce page
      soup = getCarsData.getAdPage(ad[1])
      
      # check if the car is still for sale
      match = re.search('Sidan saknas.*', soup.find("title").get_text().strip(), flags=re.IGNORECASE)
      if match:

         # the annons is removed -> continue to the next one
         # print("bla")
         continue
      else:
         print(ad[1])
         getCarsData.get_details(soup)
         getCarsData.get_volume_hp(soup)
         getCarsData.print_data(info)
         # print info


         # get all details

   #    make record in car_data table
   



