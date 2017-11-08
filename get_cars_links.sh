#!/bin/bash

PYTHON=$(which python)
WDIR="$HOME/bytbil.com"

$PYTHON $WDIR/get_cars.py > $WDIR/cron.log 2> $WDIR/cron.err
# TODO
# if the above command succeeded
# make a copy of the DB file with today's date in the filename 
# check if database copy from y-day exists, if yes: delete it
#  
