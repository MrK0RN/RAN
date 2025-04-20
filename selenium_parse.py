from selenium import webdriver
from selenium_stealth import stealth
import time
from bs4 import BeautifulSoup

class selenium_parse:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.html = None
        self.name = None

    def parse_link(self, url):
        self.driver.get(url)
        self.html = BeautifulSoup(self.driver.page_source).prettify()
        self.name = url.split("/")[-2]
        self.save_html()

    def save_html(self):
        self.save_html_to_file(self.name, self.html)

    @staticmethod
    def save_html_to_file(name, data):
        f = open("pers_files/"+name+".html", "w")
        f.write(data)
        f.close()