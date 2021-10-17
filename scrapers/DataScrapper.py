from time import sleep
from selenium import webdriver
from datetime import datetime
import pandas as pd


class DataScrapper:
    

    def __init__(self, browser):
        """When we instantiate this Class, we need to set:
        - date & time: so that we are able to traceback changes
            in our data over time with future scrapes
        - the type of browser used, just for control purposes
        - a dataframe that is going to hold each and every information
            that we scrape"""
        self.start = datetime.now()
        self.browser_ = browser
        self.df = pd.DataFrame()

    
    def start_scraper(self, path):
        """Creates our driver, sets the options that we need
        and starts the driver"""
        self.options = webdriver.ChromeOptions()
        #we need this option so that the log messages don't pollute our screen
        #is not our purpose here to debbug functionality at the moment
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=path, options=self.options)
        sleep(5)


    def get_gps_url(self, url, years):
        """This function retrieves all URLs that we need to scrape to get the data.
            Those URLs exist from 2016 until now"""
        self.hrefs = []
        for year in years:
            try:
                self.driver.get(url + year)
                sleep(5)
                # When we access the URL for a specific year, we are redirected for a specific Grand Prix that
                # ocurred that year, that's why we need to retrive two different types of HTML tags for each year:
                # the Grand Prix that we were redirected and all other circuits that happened in that year
                a_tags = self.driver.find_elements_by_xpath('//a[@class = "ms-results-subnav_item" or @class = "ms-results-subnav_item current"]')
                self.hrefs += [tag.get_attribute('href') for tag in a_tags]
            except:
                pass


    def scrape_data(self):
        """This function accesses URLs via Pandas and extract relevant specific information"""
        for url in self.hrefs:
            try: 
                # Here we access the URL using Pandas due to the easiness of accessing tables with it
                dfs = pd.read_html(url)
                # The table that we need is the first one that appears on the HTML page
                df = dfs[0]
                # We manipulate the string of the URL to get the name of circuit of the Grand Prix and
                # also the year of the information
                full_txt = url.split('/')[-2].strip().replace('-', ' ').upper()
                gp_year = url.split('/')[-3].strip()
                df['Circuit'] = ''.join([letter for letter in full_txt if not letter.isdigit()])
                df['Year'] = gp_year
                # We store the date_reference for future control (if needed)
                df['Date_Reference'] = self.start
                self.df = self.df.append(df)
            except:
                pass

    
    @staticmethod
    def treat_data(df):
        """Return input dataset with changed column names for better comprehension and removed unnecessary ones"""
        df.rename(columns={'Cla': 'Position', 'Chassis': 'Team', 'Unnamed: 1': 'Situation'}, inplace=True)
        df.drop(columns=['Unnamed: 4', 'Gap', 'Interval', 'km/h', 'Pits', 'Unnamed: 3'], inplace=True)
        return df

    
    def output_data(self, path):
        """Apply treatment function and saves the resulting dataset"""
        self.df = self.treat_data(self.df)
        self.df.to_excel(path, index=False, header=True)
        