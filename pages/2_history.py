from calendar import JANUARY
import streamlit as st
import plotly.express as px
import polars as pl
import pandas as pd
from streamlit_login_auth_ui.widgets import __login__
from pymongo import MongoClient

client = MongoClient('mongodb+srv://carboncalculator2024:zipzcwaQu1UnYTT5@carbonfootprint.febn7uz.mongodb.net/?retryWrites=true&w=majority&appName=carbonfootprint')

db = client['carbon_footprint']
collection = db['emission_data']

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
            alldoc = collection.find_one({'Username':username,'Month':y,'Year':year}, {'Total':1,'_id':0})
            if alldoc!=None:
                dict_emission[x]=alldoc["Total"]
            else:
                dict_emission[x]=0
            x=x+1
    dict_electricity={}
    dict_gas={}
    dict_wood={}
    dict_air={}
    dict_train={}
    dict_bus={}
    dict_private={}
    dict_waste={}
    dict_food={}
    x=1
    for y in dict_month:
            alldoc = collection.find_one({'Username':username,'Month':y,'Year':year}, {'Electricity':1,'Gas Connection':1,'Wood used':1,'Air travel':1,'Train travel':1,'Bus Travel':1,'Private Travel':1,'Waste generated':1,'Food':1,'_id':0})
            if alldoc!=None:
                dict_electricity[x]=alldoc["Electricity"]
                dict_gas[x]=alldoc["Gas Connection"]
                dict_wood[x]=alldoc["Wood used"]
                dict_air[x]=alldoc["Air travel"]
                dict_train[x]=alldoc["Train travel"]
                dict_bus[x]=alldoc["Bus Travel"]
                dict_private[x]=alldoc["Private Travel"]
                dict_waste[x]=alldoc["Waste generated"]
                dict_food[x]=alldoc["Food"]
            else:
                dict_electricity[x]=0
                dict_gas[x]=0
                dict_wood[x]=0
                dict_air[x]=0
                dict_train[x]=0
                dict_bus[x]=0
                dict_private[x]=0
                dict_waste[x]=0
                dict_food[x]=0
            x=x+1
    #making dictionary for line chart
   # Sample data
data = {
    "Month": ["January","February","March","April","May","June","July","August","September","October","November","December"],
    "Gas Connection":[dict_gas[1],dict_gas[2],dict_gas[3],dict_gas[4],dict_gas[5],dict_gas[6],dict_gas[7],dict_gas[8],dict_gas[9],dict_gas[10],dict_gas[11],dict_gas[12]],
    "Wood used":[dict_wood[1],dict_wood[2],dict_wood[3],dict_wood[4],dict_wood[5],dict_wood[6],dict_wood[7],dict_wood[8],dict_wood[9],dict_wood[10],dict_wood[11],dict_wood[12]],
    "Air travel":[dict_air[1],dict_air[2],dict_air[3],dict_air[4],dict_air[5],dict_air[6],dict_air[7],dict_air[8],dict_air[9],dict_air[10],dict_air[11],dict_air[12]],
    "Train travel":[dict_train[1],dict_train[2],dict_train[3],dict_train[4],dict_train[5],dict_train[6],dict_train[7],dict_train[8],dict_train[9],dict_train[10],dict_train[11],dict_train[12]],
    "Bus Travel":[dict_bus[1],dict_bus[2],dict_bus[3],dict_bus[4],dict_bus[5],dict_bus[6],dict_bus[7],dict_bus[8],dict_bus[9],dict_bus[10],dict_bus[11],dict_bus[12]],
    "Private Travel":[dict_private[1],dict_private[2],dict_private[3],dict_private[4],dict_private[5],dict_private[6],dict_private[7],dict_private[8],dict_private[9],dict_private[10],dict_private[11],dict_private[12]],
    "Waste generated":[dict_waste[1],dict_waste[2],dict_waste[3],dict_waste[4],dict_waste[5],dict_waste[6],dict_waste[7],dict_waste[8],dict_waste[9],dict_waste[10],dict_waste[11],dict_waste[12]],
    "Food":[dict_food[1],dict_food[2],dict_food[3],dict_food[4],dict_food[5],dict_food[6],dict_food[7],dict_food[8],dict_food[9],dict_food[10],dict_food[11],dict_food[12]]
}

# Create DataFrame
df = pd.DataFrame(data)

# Create a stacked bar chart using Plotly
fig = px.bar(df, x='Month', y=['Gas Connection','Wood used','Air travel','Train travel','Bus Travel','Private Travel','Waste generated','Food'], barmode='stack')
fig.update_layout(xaxis_title='Month', yaxis_title='Emission')

# Display the plotly chart
st.plotly_chart(fig)
