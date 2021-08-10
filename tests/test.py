from scrapper.house_price_scrapper import HouseInfoScraper
import pytest




scraper = HouseInfoScraper(numofitems=2,keyword="duplex")


def test_initialized_wrong_enum():
    with pytest.raises(Exception):
        HouseInfoScraper(numofitems='a',keyword="duplex")

def test_get_scrapped_url():
    so = scraper.getpagecontent()
    assert so.scrapped_url == 'https://casa.sapo.pt/duplex/pn=2'

def test_scrap_func_with_not_int():
    so = HouseInfoScraper(numofitems=57,keyword="duplex")
    assert so.getpagecount == 3


def test_scrapped_item_length():
    so = HouseInfoScraper(numofitems=10,keyword="duplex")
    val = 28
    data = so.scrap()
    assert data.shape[0] == val