from wsgiref.handlers import format_date_time
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import models
import plotly.express as px
import polars as pl
from PIL import Image
import os
import pandas as pd
from experiment import ScanImage
import pytesseract
from experiment2 import ScanImage2
from pymongo import MongoClient

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

@st.cache
def load_image(image_file):
   img = Image.open(image_file)
   return img

__login__obj = __login__(auth_token = "dk_prod_D8ZQ8GGX75M35KMST4HRTSX97QED",company_name = "Carbon Footprint Calculator",width = 200, height = 250,logout_button_name = 'Logout', hide_menu_bool = False,hide_footer_bool = False,lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()

if LOGGED_IN == True:
   
   air_travel=None
   amount_renewable=0
   gas_pipeline=0
   domestic=0
   gas_cylinder=0
   international=0
   private_travel=None
   mileage=0
   age=0
   total_distance=0
   train_travel=0
   bus_travel=0
   mealperday=0

   user = models.get_user(username)
   st.title(f"Welcome {user.username},")
   st.title("Carbon Calculator")

   month=st.selectbox("Select Month",['January','February','March','April','May','June','July','August','September','October','November','December'])
   year=st.selectbox("Select year",['2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030'],index=4)
   region=st.selectbox("Select",['Urban','Rural'])

   val = st.number_input('⚡Electricity used per month(KWh)', value = 0,min_value=0,max_value=1000)
   if val:
      electricity_bill=st.file_uploader("Upload a clear image of Electricity Bill")
      if electricity_bill:
         img = load_image(electricity_bill)
         st.image(img)

         with open(os.path.join("Electricity",electricity_bill.name),'wb') as f:
            f.write(electricity_bill.getbuffer())
         ScanImage()
         st.success("File Saved")

   gas_connection=st.selectbox("🧯Type of Gas Connection",['None','Gas Cylinder','Gas Pipeline'])
   if gas_connection=='Gas Cylinder':
      gas_cylinder=st.number_input('Number of gas cylinders used in a month',step=1,value=0,min_value=0,max_value=10)
   elif gas_connection=='Gas Pipeline':
      gas_pipeline=st.number_input('Gas Usage per month(cubic metre)',step=1,value=0,min_value=0,max_value=100)

   val2 = st.number_input('🪵Wood used weekly(kg)', value = 0,min_value=0,max_value=100)
   val2=max(val2,0)

   transport=st.multiselect("🚚Transport (one or more)",['Air Travel','Train','Bus','Private Vehicle'])
   if "Air Travel" in transport:
      air_travel=st.multiselect("🛫Type of air travel",['Domestic','International'])
      if 'Domestic' in air_travel:
         domestic=st.number_input("🛩️No. of one-way domestic flights per month",step=1,value=0,min_value=0,max_value=100)
      if 'International' in air_travel:
         international=st.number_input("✈️No. of one-way international flights per month",step=1,value=0,min_value=0,max_value=50)
   if "Train" in transport:
      train_travel=st.number_input("Distance traveled by train in a week",value=0,min_value=0,max_value=5000)

   if "Bus" in transport:
      bus_travel=st.number_input('🚌Distance traveled by Bus(Km) weekly',step=1,value=0,min_value=0,max_value=1000)
   if "Private Vehicle" in transport:
      private_travel=st.selectbox("⛽Fuel Type",['Petrol','Diesel'])
      mileage=st.number_input('Mileage',step=1,value=None,min_value=10,max_value=150)
      age=st.number_input('How old is your vehicle?',step=1,value=0,min_value=0,max_value=30)
      total_distance=st.number_input('Distance driven per day',step=1,value=0,min_value=0,max_value=400)
      PUC=st.file_uploader("Upload a clear image of PUC")
      if PUC:
         img = load_image(PUC)
         st.image(img)

         with open(os.path.join("PUC",PUC.name),'wb') as f:
            f.write(PUC.getbuffer())
         ScanImage2()
         st.success("File Saved")
   val1 = st.number_input('🗑️Waste Generated(Kg) per week', value = 0,min_value=0,max_value=100)
   val1=max(val1,0)
   waste=val1
   food_type=st.selectbox("🍽️Meal preference",['Vegeterian','Non-Vegeterian'])
   mealperday=st.number_input("Number of Meals per Day",step=1,value=0,min_value=0,max_value=10)
   renewable=st.selectbox("♻️Any type of renewable energy generated",["No","Yes"])
   if renewable=="Yes":
      amount_renewable=st.number_input("Amount of Energy Renewed(KWh)",step=1,value=0,min_value=0,max_value=1000)




   submit_button=st.button("Calculate the CO₂ Emission")
   

   if submit_button:
      total_emmision=val+gas_cylinder+gas_pipeline+domestic+international+train_travel+bus_travel+total_distance+val2+waste+mealperday

      emission_data = {
         'electricity': val,
         'gas_connection': gas_cylinder+gas_pipeline,
         'air_travel': domestic+international,
         'train_travel': train_travel,
         'bus_travel': bus_travel,
         'private_travel': total_distance,
         'wood_used': val2,
         'waste': waste,
         'food': mealperday,
         'total_emission': total_emmision,
         'month': month,
         'year': year
      }
      if(val>0):
         val=round(((val*0.82-(float)(amount_renewable))*12)/1000,2)
      if(gas_connection!=None):
         if(gas_cylinder):
            gas_cylinder=round((gas_cylinder*100*12)/1000,2)
         if(gas_pipeline):
            gas_pipeline=round((gas_pipeline*22.73*12)/1000,2)
      if(domestic>0):
         domestic=round((domestic*348.5*12)/1000,2)
      if(international>0):
         international=round((international*532.7*12)/1000,2)
      if(train_travel):
         train_travel=round((train_travel*2.49*12)/1000,2)
      if(bus_travel):
         bus_travel=round((bus_travel*0.1*52)/1000,2)
      if(private_travel!=None):
         if(private_travel=="Petrol"):
            total_distance=round((total_distance/mileage*2.2*365)/1000,2)
         if(private_travel=="Diesel"):
            total_distance=round((total_distance/mileage*2.6*365)/1000,2)
      if(val2>0):
         val2=round((val2*1.6*52)/1000,2)
      if(waste>0):
         waste=round((waste*1.49*52)/1000,2)
      if(food_type!=None):
         if(food_type=="Vegeterian"):
            mealperday=round((mealperday*0.776*365)/1000,2)
         if(food_type=="Non-Vegeterian"):
            mealperday=round((mealperday*1.552*365)/1000,2)
      total_emmision=val+gas_cylinder+gas_pipeline+domestic+international+train_travel+bus_travel+total_distance+val2+waste+mealperday
      st.success("Calculation Successful")
      st.header("Results")
      #For adding to DataBase
      client = MongoClient('mongodb+srv://carboncalculator2024:zipzcwaQu1UnYTT5@carbonfootprint.febn7uz.mongodb.net/?retryWrites=true&w=majority&appName=carbonfootprint')

      db = client['carbon_footprint']
      collection = db['emission_data']
      document = {'Username': username,'Month':month,'Year':year,'Electricity':val,'Gas Connection':gas_cylinder+gas_pipeline,'Wood used':val2,'Air travel':domestic+international,'Train travel':train_travel,'Bus Travel':bus_travel,'Private Travel':total_distance,'Waste generated':waste,'Food':mealperday,'Total':total_emmision}
      collection.insert_one(document)

       # Create a pie chart:https://plotly.com/python/pie-charts/
      df = pl.DataFrame(
         {
            "labels":['Electricity','Gas Connection','Wood used','Air travel','Train travel','Bus Travel','Private Travel','Waste generated','Food'],
            "values":[val,gas_cylinder+gas_pipeline,val2,domestic+international,train_travel,bus_travel,total_distance,waste,mealperday],
         }
      )
      #color schemes at:https://plotly.com/python/discrete-color/
      fig = px.pie(df, values='values', names='labels', title='Carbon Emmision',color_discrete_sequence=px.colors.qualitative.G10)
      fig.update_traces(textposition='inside', textinfo='percent+label')
      st.plotly_chart(fig)
      
      models.add_emission(emission_data, user)
      try:
         emission = models.get_emission(username, month, year)

         for key, value in emission.__dict__.items():
            print(f'{key}: {value}')
      except AttributeError:
         st.write("Invalid entry")

      col1, col2=st.columns(2)
      with col1:
         st.info(f"Electricity : {val} tonnes of CO₂ produced")
         st.info(f"Gas Connection : {gas_cylinder+gas_pipeline} tonnes of CO₂ produced")
         st.info(f"Air travel : {domestic+international} tonnes of CO₂ produced")
         st.info(f"Train travel : {train_travel} tonnes of CO₂ produced")
         st.info(f"Bus Travel : {bus_travel} tonnes of CO₂ produced")
      with col2:
         st.info(f"Private Travel : {total_distance} tonnes of CO₂ produced")
         st.info(f"Wood used : {val2} tonnes of CO₂ produced")
         st.info(f"Waste generated : {waste} tonnes of CO₂ produced")
         st.info(f"Food : {mealperday} tonnes of CO₂ produced")

      #creating dictionary for all values
      dict = {
         'Electricity':val,
         'Gas Connection':gas_cylinder+gas_pipeline,
         'Wood used':val2,
         'Air travel':domestic+international,
         'Train travel':train_travel,
         'Bus Travel':bus_travel,
         'Private Travel':total_distance,
         'Waste generated':waste,
         'Food':mealperday,
      }

      st.subheader("Your Total Carbon Emission(in tonnes of CO₂ produced)")
      st.info(f"Your Total Carbon Emission: {total_emmision} tonnes of CO₂ produced")
      if(region=='Urban'):
         if(total_emmision>2.5):
               st.warning(f"Your average CO₂ consumption is {((total_emmision-2.5)/2.5)*100}% above Average")
         else:
               st.info(f"Your average CO₂ consumption is {((2.5-total_emmision)/2.5)*100}% below Average")
         st.warning("Urban area average CO₂ consumption is 2.5 tonnes of CO₂")
         st.success("All Details are recorded in our records")
      if(region=='Rural'):
         if(total_emmision>0.85):
               st.warning(f"Your average CO₂ consumption is {round(((total_emmision-0.85)/0.85)*100,2)}% above Average")
         else:
               st.info(f"Your average CO₂ consumption is {((round(0.85-total_emmision)/0.85)*100,2)}% below Average")
         st.warning("Rural area average CO₂ consumption is 0.85 tonnes of ")


      #upload data
