from DataScrapper import DataScrapper
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd


load_dotenv()
driver_path = os.getenv('CHROMEDRIVER_PATH')
output_path = os.getenv('OUTPUT_BASE_PATH')

base_url = os.getenv('BASE_URL')


scraper = DataScrapper('chrome')

scraper.start_scraper(driver_path)
scraper.get_gps_url(base_url, pd.date_range('2016-01-01', datetime.now(), freq='YS').strftime("%Y").tolist())
scraper.scrape_data()
scraper.output_data(output_path + 'scrapper_result.xlsx')
scraper.driver.close()
