from calendar import JANUARY
import streamlit as st
import plotly.express as px
import polars as pl
import pandas as pd
import models
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(page_title="History",page_icon=":footprints:",layout="wide")
__login__obj = __login__(auth_token = "dk_prod_D8ZQ8GGX75M35KMST4HRTSX97QED",company_name = "Carbon Footprint Calculator",width = 200, height = 250,logout_button_name = 'Logout', hide_menu_bool = False,hide_footer_bool = False,lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()
# dictionary of months
dict_month=['January','February','March','April','May','June','July','August','September','October','November','December']

if LOGGED_IN == True:
    st.header("Statistics")
    st.subheader("Last 1 year data")
    #dictionary storing value of emission
    year=st.selectbox("Select year",['2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030'],index=4)
    dict_emission={}
    x=1
    for y in dict_month:
        try:
            emissions=models.get_emission(username,y,year)
            dict_emission[x]=emissions.total_emission
            x=x+1
        except AttributeError:
            dict_emission[x]=0
            x=x+1
    #making dictionary for line chart
    df = pd.DataFrame(dict(
        Month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12],
        Total_Emission = [dict_emission[1],dict_emission[2],dict_emission[3],dict_emission[4],dict_emission[5],dict_emission[6],dict_emission[7],dict_emission[8],dict_emission[9],dict_emission[10],dict_emission[11],dict_emission[12]]
    ))
    fig = px.line(df, x="Month", y="Total_Emission", title="Emission in {year}")
    st.plotly_chart(fig)
    print(dict_emission)