import streamlit as st

stremlitbuilder = None

class StreamlitComponentBuilder:
    
    def st_header(self,**kwargs):
        return st.header(**kwargs)
    
    def st_selectbox(self,**kwargs):
        return st.selectbox(**kwargs)
    
    def st_radio(self,**kwargs):
        return st.radio(**kwargs)
    
    def st_textinput(self,**kwargs):
        return st.text_input(**kwargs)
    
    def st_slider(self,**kwargs):
        return st.slider(**kwargs)
    
    def st_button(self,**kwargs):
        return st.button(**kwargs)
    
    def st_form_button(self,**kwargs):
        return st.form_submit_button(**kwargs)
    
    def st_subheader(self,**kwargs):
        return st.subheader(**kwargs)
    
    
def create():
    global stremlitbuilder
    stremlitbuilder = StreamlitComponentBuilder()
    return stremlitbuilder

def st_expander_df(df):
    expander = st.expander("See Output Preview")
    return expander.table(df)