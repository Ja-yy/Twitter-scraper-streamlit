import time

import pandas as pd
import streamlit as st
from selenium.common import exceptions


def twitter_scraper_main(
    twitterInstance, driver, username, password, search_term, max_scroll
):
    last_position = None
    end_of_scroll_region = False
    unique_tweets = set()
    tweet_list = list()
    logged_in = twitterInstance.login(email=username, password=password)

    if not logged_in:
        return

    time.sleep(2)
    twitterInstance.search_bar(search_term)
    twitterInstance.select_tab()
    si = 0
    while not end_of_scroll_region:
        cards = twitterInstance.collect_tweet_card(driver)
        for card in cards:
            try:
                tweet = twitterInstance.scrap_tweet_card(card)
            except exceptions.StaleElementReferenceException:
                continue
            if not tweet:
                continue
            tweet_id = twitterInstance.generate_tweet_id(tweet)
            if tweet_id not in unique_tweets:
                unique_tweets.add(tweet_id)
                tweet_list.append(tweet)
        si += 1
        if si <= max_scroll:
            last_position, end_of_scroll_region = twitterInstance.scroll_down_page(
                last_position
            )
        else:
            end_of_scroll_region = True
    st.write(f"Total Handlers scraped... {len(tweet_list)}")
    df = pd.DataFrame(tweet_list, columns=["Username", "handler", "URL"])
    df = df.reset_index(drop=True)
    driver.quit()
    return df
