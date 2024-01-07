import streamlit as st
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_scripts.twitter.twitter_bot_helper import TwitterBotHelper
from selenium_scripts.utils.driver import Driver

twitterInstance = None


class TwitterBot(TwitterBotHelper):
    def __init__(self, headless=False, browser_name="chrome"):
        self.driver = Driver(headless, browser_name).get_driver()

    def redirect_to_login(self):
        URL = "https://twitter.com/i/flow/login"
        try:
            self.driver.get(URL)
            return self.driver
        except AttributeError:
            return "Driver is not set"

    def login(self, email, password):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            ).send_keys(email, Keys.RETURN)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            ).send_keys(password, Keys.RETURN)
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be("https://twitter.com/home")
            )
            return self.driver
        except exceptions.TimeoutException:
            st.error("Timeout while waiting for Login screen", icon="🚨")

    def search_bar(self, search_term):
        try:
            xpath_search = '//input[@aria-label="Search query"]'
            search_input = self.driver.find_element(By.XPATH, xpath_search)
            search_input.send_keys(search_term)
            search_input.send_keys(Keys.RETURN)
        except exceptions.TimeoutException:
            return st.error("Timeout while waiting for Login screen", icon="🚨")

    def select_tab(self, tab="People"):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@data-testid="ScrollSnap-List"]')
                )
            )
            ScrollSnap_List = self.driver.find_element(
                By.XPATH, '//div[@data-testid="ScrollSnap-List"]'
            )
            tab_xpath = f'//div/span[text()= "{tab}"]'
            select_tab = ScrollSnap_List.find_element(By.XPATH, tab_xpath)
            select_tab.click()
            return None
        except exceptions.TimeoutException:
            return st.error("Timeout while waiting for Login screen", icon="🚨")


def create(headless=False, browser_name="chrome"):
    global twitterInstance
    twitterInstance = TwitterBot(headless, browser_name)
    return twitterInstance
