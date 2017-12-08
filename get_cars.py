#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
import os
import time
import codecs
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import sqlite3 as lite
from operator import itemgetter
from datetime import datetime, timedelta
from random import *

# from IPython.core.debugger import Tracer
# from HTMLParser import HTMLParser

# get rid of a warning message
requests.packages.urllib3.disable_warnings()



class getCars:


   def connectDB(self):

      db_file = dir_path + "/bytbil.com.sqlite"
      return  lite.connect(db_file)


   def getPage(self, url):
      # make a request and get the whole page in data object
      r = requests.get(url)
      data = r.text
      #print data.encode('utf-8').strip()
      return data

   def getLinksList(self, data):

      cars = list()

      # get the BeautifulSoup object
      soup = BeautifulSoup(data, "html.parser")

      # get all the car links from the page
      for h3s in soup.find_all("h3", class_="uk-text-truncate car-list-header hidden-small-and-below"):
         cars.append(h3s.find('a').get('href'))
      return cars
 
if __name__ == "__main__":


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
   url = "https://www.bytbil.com/bil?Page="
   b_link = "https://www.bytbil.com"

   dir_path = os.path.dirname(os.path.realpath(__file__))


   # define a list to store the links
   cars_links = list()


   # define a counter; set it to 1
   c = 0

   # connect to db and create a  cursor
   db = getCars.connectDB()
   cur = db.cursor()

   # set current date
   currentDate = datetime.today().strftime('%Y-%m-%d')

   stop = False

   #     #    #    ###  #     #
   ##   ##   # #    #   ##    #
   # # # #  #   #   #   # #   #
   #  #  # #     #  #   #  #  #
   #     # #######  #   #   # #
   #     # #     #  #   #    ##
   #     # #     # ###  #     #

   while stop == False:


      # combine the url with the counter
      p_url = url + str(c)
      #print url

      # get the page html
      page = getCars.getPage(p_url)

      # get the cars links from a page
      res = getCars.getLinksList(page)

      if len(res) == 0:
         break
      else:
         # iterate over the links
         for link in res:

            link = b_link + link.strip()
            # define the query
            query = u"INSERT INTO car_links (link, date, annons_id) VALUES (\'%s\', \'%s\', \'%s\');" % (link, currentDate, "n")
            
            try:

               cur.execute(query)
               #increment the counter
               c += 1
            except Exception as e:
               
               # print e
               print link
               stop = True
      time.sleep(randint(1, 9))

   db.commit()

   log_file = dir_path + "/get_cars_log.csv"
   out = open(log_file, 'a')
   out.write(currentDate + "," + str(c) + '\n')
   # print currentDate + "," + str(c) + " new links found"




