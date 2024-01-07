from pathlib import Path

import streamlit as st

from stremlitbuilder import st_builder

tab1builder = None


class Tab:
    """Class for Tab"""

    extended_view = None

    def __init__(self, md_path, extended_view=None):
        self.intro_markdown = Path(md_path).read_text()

        if extended_view:
            self.extended_view = extended_view

    def view(self):
        st.markdown(self.intro_markdown, unsafe_allow_html=True)
        if self.extended_view:
            self.extended_view()


def create():
    global tab1builder
    stremlitbuilder = st_builder.create()
    return stremlitbuilder
