from time import sleep

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TwitterBotHelper:
    def collect_tweet_card(self, driver, lookback_limit=25):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@aria-label="Timeline: Search timeline"]')
            )
        )
        page_cards = driver.find_elements(
            By.XPATH,
            '//div[@data-testid="primaryColumn"]//div[@data-testid="cellInnerDiv"]',
        )[-lookback_limit:]
        return page_cards

    def scrap_tweet_card(self, card):
        user = ""
        handle = ""
        url = ""

        try:
            user_elem = card.find_element(By.XPATH, ".//span")
            user = user_elem.text
        except exceptions.NoSuchElementException:
            pass

        try:
            handle_elem = card.find_element(By.XPATH, './/span[contains(text(), "@")]')
            handle = handle_elem.text.replace("@", "")
            url = "https://twitter.com/" + handle
        except exceptions.NoSuchElementException:
            pass

        if user and handle and url:
            tweet = (user, handle, url)
            return tweet

    def generate_tweet_id(self, tweet):
        return "".join(tweet)

    def scroll_down_page(
        self, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5
    ):
        end_of_scroll_region = False
        try:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            sleep(num_seconds_to_load)
            curr_position = self.driver.execute_script("return window.pageYOffset;")
            if curr_position == last_position:
                if scroll_attempt < max_attempts:
                    end_of_scroll_region = True
                else:
                    self.scroll_down_page(
                        last_position, curr_position, scroll_attempt + 1
                    )
            last_position = curr_position
        except Exception as e:
            print(f"Error while scrolling: {e}")
            end_of_scroll_region = True
        return last_position, end_of_scroll_region
