#!/bin/bash

PYTHON=$(which python)

$PYTHON $HOME/bytbil.com/get_cars.py 
# TODO
# if the above command succeeded
# make a copy of the DB file with today's date in the filename 
# check if database copy from y-day exists, if yes: delete it
#  
