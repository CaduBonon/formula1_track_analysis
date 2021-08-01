from Scraper import CircuitScraper
import os
from dotenv import load_dotenv 


load_dotenv()
driver_path = os.getenv('CHROMEDRIVER_PATH')
output_path = os.getenv('OUTPUT_BASE_PATH')

circuit_url = 'https://www.racefans.net/f1-information/going-to-a-race/'


# Gerando dados técnicos de circuitos
c_scraper = CircuitScraper('chrome')

c_scraper.start_scraper(driver_path, circuit_url)

c_scraper.get_circuits_url()

c_scraper.scrape_data(driver_path)

c_scraper.output_data(output_path + 'circuits_info.xlsx')

c_scraper.driver.close()


# Gerando dados de vitórias de pilotos
