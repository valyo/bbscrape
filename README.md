# bbscrape

Scrape bytbil.com every day and:

	1. put all new ads links in a DB
	2. set today's date as an end_date for each ad that had disappeared
	3. scrape new adds and add a DB record with all the details about the car

# Database 

## bytbil.com.sqlite

contains the following tables:

### car_links

|Field      | Description      
| --------- | ------------
| link_id   | a PRIMARY KEY id
| link      | the actual ad link
| date      | date of collecting
| annons_id | a "n" or "y" flag indicating if the ad is already scraped; set to "n" when link collected
end_date | the date on which check_ads.py finds that the ad is missing from bytbil.com

*get_links.py* inserts new links into this table with default **annons_id**="n" and an empty **end_date**

*check_ads.py* updates records where the **link** points to expired ad, by setting **end_date** to the current date



### cars_data

Field | Description
--- | ---
annons_id | same as link_id in cars_links table
feature 1 | features
feature 2 | ...
... | ...
feature N | last feature

*scrape_cars.py* inserts new records in the following way:

	1. select all entries from car_links where **annons_id**="n"
	2. for each link that does point to an existing ad: scrape as much as possible and insert a record in cars_data
	3. if the INSERT query is successful, UPDATE car_links by setting **annons_id**="y" for the record with the corresponding **ink_id**

