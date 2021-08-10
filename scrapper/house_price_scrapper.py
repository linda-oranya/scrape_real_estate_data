from typing import List
from bs4 import BeautifulSoup
import requests
import pandas as pd
import itertools
import requests
import time


class HouseInfoScraper:
    """
    The HouseInfoScraper class scrapes house details of houses on the casa.sapo.lt website
    """
    def __init__(self, keyword, numofitems) -> None:
        self.keyword = keyword
        self.numofitems = numofitems


    def getpagecount(self, numofitems: int) -> int:
        """
        Gets the page numbers to be scrapped from the number of items
        """
        pages = round(numofitems / 27) + 1
        return pages

    def checkinput(self, object, instance) -> None:
        """
        Validates that the number of items is an integer type
        """
        if not isinstance(object, instance):
            raise ValueError(f"Expected {instance} instead of {object}")

    def getpagecontent(self, url) -> requests:
        """
        Gets the page content of pages
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
            "Referer": "http://www.google.com/", 
            "Sec-Ch-Ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"", 
            "Sec-Ch-Ua-Mobile": "?0", 
            "Sec-Fetch-Dest": "document", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-Site": "cross-site", 
            "Sec-Fetch-User": "?1", 
            "Upgrade-Insecure-Requests": "1"
        }

        send_proxies = {'http':'0.0.0.0:80','https':'0.0.0.0:80'}

        read_site = requests.get(url, headers=headers,proxies=send_proxies)
        return read_site.content

  
    def scrap(self,url) -> BeautifulSoup:
        """
        Gets the soup content of the url
        """
        self.checkinput(self.numofitems, int)
        url = url
        content = self.getpagecontent(url)
        soup = BeautifulSoup(content,"html.parser")
        return soup
    
    def scrape_price(self) -> List:
        """
        Scrapes prices of house from the website
        """
        prices = [] 
        pages = self.getpagecount(self.numofitems)
        for page in range(1,pages): 
            time.sleep(5)       
            soup = self.scrap(url=f"https://casa.sapo.pt/{self.keyword}/pn={page}")
            house_containers = soup.find_all("div", class_="searchResultProperty")

            if house_containers != []:
                for container in house_containers:
                    price = container.find_all("span")[2].text
                    if price == "Contacte Anunciante":
                        price = container.find_all("span")[3].text
                        if price.find("/") != -1:
                            price = price[0 : price.find("/") - 1]
                    if price.find("/") != -1:
                        price = price[0 : price.find("/") - 1]

                    price_ = [
                        int(price[s]) for s in range(0, len(price)) if price[s].isdigit()
                    ]
                    price = ""
                    for x in price_:
                        price = price + str(x)
                    prices.append(price)
            else:
                pass
        print("price",len(prices))
        return prices

    def scrape_location(self) -> List:
        """Scrapes the location of the house from the website"""
        zone = []
        pages = self.getpagecount(self.numofitems)
        for page in range(1,pages):
            time.sleep(5)        
            soup = self.scrap(url=f"https://casa.sapo.pt/{self.keyword}/pn={page}")
            house_containers = soup.find_all("div", class_="searchResultProperty")
            if house_containers != []:
                for container in house_containers:
                    location = container.find_all("p", class_="searchPropertyLocation")[0].text
                    location = location[7 : location.find(",")]
                    zone.append(location)
            else:
                pass
        print("zone",len(zone))
        return zone

    def scrape_title(self) -> List:
        """
        Scrapes the title of the house from the website
        """
        titles = []
        pages = self.getpagecount(self.numofitems)
        print(f"scrapping for {pages} pages")
        for page in range(1,pages): 
            time.sleep(5)       
            soup = self.scrap(url=f"https://casa.sapo.pt/{self.keyword}/pn={page}")
            house_containers = soup.find_all("div", class_="searchResultProperty")
            if house_containers != []:
                for container in house_containers:
                    name = container.find_all("span")[0].text
                    titles.append(name)
            else:
                pass
        print("title",len(titles))
        return titles  


    def scrape_condition(self) -> List:
        """
        Scrapes house condition from the website
        """
        condition = []
        pages = self.getpagecount(self.numofitems)
        for page in range(1,pages):
            time.sleep(5)        
            soup = self.scrap(url=f"https://casa.sapo.pt/{self.keyword}/pn={page}")
            house_containers = soup.find_all("div", class_="searchResultProperty")
            if house_containers != []:
                for container in house_containers:
                    status = container.find_all("p")[5].text
                    condition.append(status)
            else:
                pass
        print("condition",len(condition))
        return condition

    def scrape_area(self) -> List:
        """
        Scrapes the area of the house
        """
        areas = []
        pages = self.getpagecount(self.numofitems)
        for page in range(1,pages): 
            time.sleep(5)       
            soup = self.scrap(url=f"https://casa.sapo.pt/{self.keyword}/pn={page}")
            house_containers = soup.find_all("div", class_="searchResultProperty")
            if house_containers != []:
                for container in house_containers:
                    m2 = container.find_all("p")[9].text
                    if m2 != "-":
                        m2 = m2.replace("\xa0", "")
                        m2 = float("".join(itertools.takewhile(str.isdigit, m2)))
                        areas.append(m2)

                    else:
                        m2 = container.find_all("p")[7].text
                        if m2 != "-":
                            m2 = m2.replace("\xa0", "")
                            m2 = float("".join(itertools.takewhile(str.isdigit, m2)))
                            areas.append(m2)
                        else:
                            areas.append(m2)

            else:
                pass
        print("area",len(areas))
        return areas


    def collect_info(self) -> pd.DataFrame:
        """
        Collects information gathered to a dataframe
        """
        cols = ["Title", "Zone", "Price", "Size (m²)", "Status"]

        df = pd.DataFrame(
            {
                "Title": self.scrape_title(),
                "Price": self.scrape_price(),
                "Size (m²)": self.scrape_area(),
                "Zone": self.scrape_location(),
                "Status": self.scrape_condition()
            }
        )[cols]

        print("You scraped {} pages containing {} properties.".format(self.numofitems, self.keyword))
        return df


class Clean_df(HouseInfoScraper):
    """
    The Clean_df class cleans the scraped items in the dataframe
    """
    def __init__(self, keyword,numofitems) -> None:
        self.keyword = keyword
        super().__init__(keyword,numofitems)

    def clean_scrapped_df(self) -> pd.DataFrame:
        """
        Cleans the scrapped data in the dataframe
        """
        df = HouseInfoScraper.collect_info(self)
        df['Title'] = df['Title'].replace({"":self.keyword})
        df['Price'] = df['Price'].fillna(df['Price'].mean())
        df['Zone'] = df['Zone'].fillna('Missing')
        df['Status'] = df['Status'].fillna('Missing')
        df['Category'] = self.keyword
        return df


keywords = ["Apartment","Duplex","Land","Office","Shop"]

q = Clean_df(numofitems=10,keyword='duplex')
df = q.clean_scrapped_df()
df.to_csv(f'Duplex.csv')
