from pymongo import MongoClient
import streamlit as st

client = MongoClient('mongodb+srv://carboncalculator2024:zipzcwaQu1UnYTT5@carbonfootprint.febn7uz.mongodb.net/?retryWrites=true&w=majority&appName=carbonfootprint')

db = client['carbon_footprint']
collection = db['signup']

# name = st.text_input("Name", value=None)
# pas = st.text_input("Password", value=None)
# submit = st.button("Submit")

## for inserting into collection

# if submit:

#     document = {'name':name,'City':pas}
#     inserted_document = collection.insert_one(document)
#     st.success("Successfully Added")
#     client.close()

# for people in collection.find():
#     st.write(people)


## for finding by keys 

alldoc = collection.find({'Name': 'Kunal'}, {'Name':1,'_id':0})
print(alldoc.count())
for item in alldoc:
    print(item)


## for showing database

# allData = client.list()
# print(allData)
# print(db.list_collection_names())
