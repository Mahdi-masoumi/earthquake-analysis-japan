from request import get_data_from_api
from emsc_crawler import run_emsc_scraper
from geofon_scraper import run_geofon_scraper


def scrape():
    get_data_from_api()
    run_emsc_scraper()
    run_geofon_scraper()
