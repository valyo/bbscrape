#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
import codecs
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import sqlite3 as lite
from operator import itemgetter
from datetime import datetime, timedelta

# from IPython.core.debugger import Tracer
# from HTMLParser import HTMLParser

# get rid of a warning message
requests.packages.urllib3.disable_warnings()



class getCarsData:


   def connectDB(self):

	   return  lite.connect('bytbil.com.sqlite')


   def getAdPage(self, url):
      
      # make a request and get the whole page in data object
      r = requests.get(url)
      data = r.text
      #print data.encode('utf-8').strip()
      return data

   def getAdsLinksList(self,cur):
      
      query = "SELECT * FROM car_links WHERE annons_id = 'n';"
      cur.execute(query)
      link_id, link = cur.fetchone()
      link = json.loads(link)
      return link



   def getLinksList(self, data):

      cars = list()

      # get the BeautifulSoup object
      soup = BeautifulSoup(data, "html.parser")

      # get all the car links from the page
      for h3s in soup.find_all("h3", class_="uk-text-truncate car-list-header hidden-small-and-below"):
         cars.append(h3s.find('a').get('href'))
      return cars
 
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
   print ads
   # for l in links
   #    get the annouce page
      # ad = getCarsData.getAdPage(l)
   #    get all details
   #    make record in car_data table
   



