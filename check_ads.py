#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrape_cars import getCarsData
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



class checkAds:


   def connectDB(self):

      db_file = dir_path + "/bytbil.com.sqlite"
      return  lite.connect(db_file)


   def match_missing(self,soup):

      match = re.search('Sidan saknas.*', soup.find("title").get_text().strip(), flags=re.IGNORECASE)
      return match


 
if __name__ == "__main__":


   checkAds = checkAds()
   getCarsData = getCarsData()


   ### #     # ### #######
    #  ##    #  #     #
    #  # #   #  #     #
    #  #  #  #  #     #
    #  #   # #  #     #
    #  #    ##  #     #
   ### #     # ###    #


   dir_path = os.path.dirname(os.path.realpath(__file__))


   # connect to db and create a  cursor
   db = checkAds.connectDB()
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

   # get all links saved in DB which have not expired
   query = u"SELECT link FROM car_links WHERE end_date IS NULL;"
   cur.execute(query)
   res = cur.fetchall()
   
   
   for lnk in res:
      
      soup = getCarsData.getAdPage(lnk[0])
      try:
         m = checkAds.match_missing(soup)
         if m:
            query = u"UPDATE car_links SET end_date = '%s' WHERE link = '%s';" % (currentDate, lnk[0])
            cur.execute(query)
            db.commit()
      except Exception as e:
         print lnk[0]
      time.sleep(2)
   