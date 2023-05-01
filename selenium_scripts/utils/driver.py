from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from fake_headers import Headers
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FirfoxOption
import streamlit as st
from selenium import webdriver


BROWSER_OPTIONS = {
    "chrome": ChromeOption,
    "firefox": FirfoxOption,
}

driverInstance = None

class Driver:
    def __init__(self, headless=False, browser_name="chrome"):
        self.headless = headless
        self.browser_name = browser_name
        
    def set_properties(self, browser_option):
        ua = Headers().generate
        arguments = [
            '--incognito',
            '--start-maximized',
            '--disable-notifications',
            f'user-agent={ua}'
        ]
        if self.headless:
            arguments.append('--headless')
        for arg in arguments:
            browser_option.add_argument(arg)
        return browser_option
    
    def get_driver(self):
        try:
            self.browser_name = self.browser_name.strip().title()
            options = self.set_properties(browser_option=BROWSER_OPTIONS[self.browser_name.lower()]())
            if self.browser_name.lower() == "chrome":
                options.add_experimental_option("detach", True)
                driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            elif self.browser_name.lower() == "firefox":
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
            else:
                return st.error("Browser not supported!")
            return driver
        except Exception as ex:
            return ex

def create():
    global driverInstance
    driverInstance = Driver()
    return driverInstance

