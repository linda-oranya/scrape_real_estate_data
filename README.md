### Scrape Real Estate listings from Sapo website
The project is to scrape sapo website.

Usage
This libary can be used when the key interest is to retrieve information from Sapo real estate page.

The package allows you to input number of items to scrape. 
Maximun number that can be scrapped per page is 27.

Sample codes

```from HouseInfoScraper import collect_info

 scraper = collect_info(numofitems=10,keyword='duplex')
 