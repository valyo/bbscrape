#!/bin/bash

PYTHON=$(which python)
WDIR="$HOME/bytbil.com"


# scrape bytbil.com page-by-page and add new ads links to DB
echo "get_cars log" > $WDIR/cron.log
$PYTHON $WDIR/get_cars.py >> $WDIR/cron.log 2> $WDIR/cron.err


# check for ads that have gone away and set end_date
# for them in DB
echo "check_ads log" >> $WDIR/cron.log
$PYTHON $WDIR/check_ads.py >> $WDIR/cron.log 2> $WDIR/cron.err


# TODO
# if the above command succeeded
# make a copy of the DB file with today's date in the filename 
# check if database copy from y-day exists, if yes: delete it
#  
