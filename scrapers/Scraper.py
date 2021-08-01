from datetime import datetime
from os import stat
from time import sleep
from selenium import webdriver
import pandas as pd
import re


class CircuitScraper:
    

    def __init__(self, browser):
        self.start = datetime.now
        self.browser_ = browser
        self.df = pd.DataFrame()


    def start_scraper(self, path, webpage):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=path, options=self.options)
        self.driver.get(webpage)
        sleep(5)


    def get_circuits_url(self):
        # a_tags = self.driver.find_elements_by_xpath('//a[contains(@href, "circuit-information") or contains(@href, "track-information")]')
        a_tags = self.driver.find_elements_by_xpath('//a[contains(@href, "going-to-a-race") and not(contains(@title, "Fan"))]')
        self.hrefs = list(set([a_tag.get_attribute('href') for a_tag in a_tags]))

    
    @staticmethod
    def treat_name(txt):
        txt1 = re.sub(u"\u2013", "-", txt).split('-')[0]
        txt2 = txt1.replace('-', '')
        txt3 = txt2.replace(',', '')
        txt4 = txt3.replace('circuit', '')
        txt5 = txt4.replace('street', '')
        txt6 = txt5.replace('track', '')
        txt7 = txt6.replace('information', '')
        txt8 = txt7.strip()
        return txt8


    def scrape_data(self, path):
        for url in self.hrefs:
            aux_driver = webdriver.Chrome(executable_path=path, options=self.options)
            aux_driver.get(url)
            sleep(5)
            try:
                data_table = aux_driver.find_element_by_xpath('//table[@class = "thin"]')
                data_trs = data_table.find_elements_by_xpath('//tr')
                data_tds = [tr.find_elements_by_xpath('./td') for tr in data_trs]
                dict_ = {}
                for td in data_tds:
                    try:
                        dict_[td[0].text] = [td[1].text]
                    except:
                        pass
                try:
                    dict_["Track_name"] = aux_driver.find_element_by_xpath('//div[@class = "entry-content"]//strong').text
                    if dict_["Track_name"] == 'Lap data':
                        name_txt = aux_driver.find_element_by_xpath('//h1[@class = "entry-title"]').text
                        dict_["Track_name"] = self.treat_name(name_txt)
                    else:
                        pass
                except:
                    pass
                aux_df = pd.DataFrame.from_dict(data=dict_)
                self.df = self.df.append(aux_df, ignore_index=True)
            except:
                pass
            aux_driver.close()

    
    def output_data(self, path):
        self.df.to_excel(path, index=False, header=True)
        