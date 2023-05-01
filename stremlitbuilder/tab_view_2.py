from helper.enums import BrowserEnum, YesNoEnum
import streamlit as st

from view import base_tab
from view.base_tab import Tab
from stremlitbuilder.st_builder  import st_expander_df
from selenium_scripts.twitter import bot_twiter
from helper.download_button import convert_df
from selenium_scripts.twitter.twitter_scraper_main import twitter_scraper_main

tab1builder = None
class Tab2(Tab):
    """A class that represents the second tab of the Streamlit application."""

    def __init__(self,stremlitbuilder) -> None:
        self.stremlitbuilder = stremlitbuilder

    def column_1(self):
        self.stremlitbuilder.st_subheader(body="Configuration")
        browser_name = self.stremlitbuilder.st_selectbox(
            label="Which browser would you like to select?",
            options=BrowserEnum._member_names_,
        )
        headless = self.stremlitbuilder.st_radio(
            label="Do you want hide browser window", options=YesNoEnum._member_names_
        )
        return browser_name,headless

    def column_2(self):
        self.stremlitbuilder.st_subheader(body="Credential")
        email = self.stremlitbuilder.st_textinput(label="Enter your email")
        password = self.stremlitbuilder.st_textinput(label="Enter your password", type="password")
        return email,password
    
    def column_3(self):
        self.stremlitbuilder.st_subheader(body="Filter Options")
        search_term = self.stremlitbuilder.st_textinput(label="Enter search term")
        # select_tab = self.stremlitbuilder.st_radio(label="Which tab do you want to scrap?",
        #     options=SearchTabEnum._member_names_,
        #     )
        scroll = self.stremlitbuilder.st_slider(label="How many times you want to scroll?", min_value=0,max_value= 50,step= 5)
        return search_term,scroll
    
    def create_view(self):
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            with st.form(key="myform"):
                container = st.container()
                colu_1, colu_2, colu_3 = st.columns(3)

                with container:
                    with colu_1:
                        browser_name,headless = self.column_1()
                    with colu_2:
                        email,password = self.column_2()
                    with colu_3:
                        search_term,scroll = self.column_3()

                submit_button = self.stremlitbuilder.st_form_button(label="Scrap")

        return submit_button,browser_name,headless,email,password,search_term,scroll
    

def create():
    stremlitbuilder = base_tab.create()
    global tab1builder
    tab1builder = Tab2(stremlitbuilder) # will call tab2 create_view and provide layout for tab 2
    return tab1builder.create_view()


def tab_view():
    (
        submit_button,
        browser_name,
        headless,
        email,
        password,
        search_term,
        scroll,
    ) = create()
    try:
        if submit_button:
            inputs = [email, password, search_term]
            input_names = ["Email", "Password", "Search term"]
            for input, name in zip(inputs, input_names):
                if not input:
                    st.warning(f"Please enter a value for {name}.", icon="⚠️")
                    st.stop()
            twitterInstance = bot_twiter.create( headless=True,browser_name=browser_name,) if headless == "Yes" else bot_twiter.create(browser_name=browser_name, headless=False)
            driver = twitterInstance.redirect_to_login()
            try:
                df = twitter_scraper_main(
                    twitterInstance=twitterInstance,
                    driver=driver,
                    username=email,
                    password=password,
                    search_term=search_term,
                    # tab=select_tab,
                    max_scroll=scroll,
                )
            except Exception as e:
                st.error(f"An error occurred while running the script: {e}")
                st.stop()
            st.success("Completed", icon="✅")
            st.download_button(
                label="Download",
                data=convert_df(df),
                file_name="Scrape-Twitter-Handlers.csv",
                mime="text/csv",
            )
            st_expander_df(df)
    except Exception as e:
        st.error(f"An error occurred while running code: {e}")
        st.stop()
            
    
