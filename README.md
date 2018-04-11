# bbscrape

Scrape bytbil.com every day and:

	1. put all new ads links in a DB
	2. set today's date as an end_date for each ad that had disappeared
	3. scrape new adds and add a DB record with all the details about the car

# Database 

## bytbil.com.sqlite

contains the following tables:

### car_links

Field | Description
--- | ---
link_id | a PRIMARY KEY id
link | the actual ad link
date | date of collecting
annons_id | a "n" or "y" flag indicating if the ad is already scraped; set to "n" when link collected
end_date | the date on which check_ads.py finds that the ad is missing from bytbil.com



