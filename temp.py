import sqlite3 as lite
from datetime import datetime, timedelta

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
