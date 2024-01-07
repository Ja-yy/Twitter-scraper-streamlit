import streamlit as st

from constant import MD_PATH_TAB_1, MD_PATH_TAB_2
from stremlitbuilder.tab_view_2 import tab_view
from view.base_tab import Tab


def main():
    st.set_page_config(layout="wide")
    st.title("Twitter Scraper Bot 🤖")
    # tab1,tab2,tab3,tab4,tab5 = st.tabs(["Home","Twitter Handle Scraper","Tweet Scraper","Profile Scraper","CSVvvvv"])
    tab_1 = Tab(MD_PATH_TAB_1)
    tab_2 = Tab(MD_PATH_TAB_2, tab_view)

    tabs_view = [
        {"name": "Home", "view": tab_1.view},
        {"name": "Twitter Handle Scraper", "view": tab_2.view},
    ]

    tabs = st.tabs([tabs.get("name", "tab") for tabs in tabs_view])

    # with tabs
    tabs_len = len(tabs)

    for i in range(0, tabs_len):
        with tabs[i]:
            tabs_view[i]["view"]()


if __name__ == "__main__":
    main()
