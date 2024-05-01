import re
from trycourier import Courier
import secrets
from argon2 import PasswordHasher
import requests
import json
from pymongo import MongoClient

client = MongoClient('mongodb+srv://carboncalculator2024:zipzcwaQu1UnYTT5@carbonfootprint.febn7uz.mongodb.net/?retryWrites=true&w=majority&appName=carbonfootprint')

db = client['carbon_footprint']
collection = db['signup']

ph = PasswordHasher()

def check_usr_pass(username: str, password: str) -> bool:
    """
    Authenticates the username and password.
    """
    try:
        alldoc = collection.find_one({'Username':username,'Password':password}, {'Name':1,'_id':0})
        total = alldoc["Name"]
        return True    
    except:
        pass
    return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str,) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    try:
        alldoc = collection.find({'Email': email_sign_up})
        # total = alldoc["Email"]
        # print(total)
        if alldoc==None:
            return True
        return False  
    except:
        return True
    # authorized_user_data_master = list()
    # with open("secret_auth.json", "r") as auth_json:
    #     authorized_users_data = json.load(auth_json)

    #     for user in authorized_users_data:
    #         authorized_user_data_master.append(user['email'])

    # if email_sign_up in authorized_user_data_master:
    #     return False
    # return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    try:
        alldoc = collection.find_one({'Username':username_sign_up,}, {'Name':1,'_id':0})
        total = alldoc["Name"]
        return False    
    except:
        return True
    # authorized_user_data_master = list()
    # with open("secret_auth.json", "r") as auth_json:
    #     authorized_users_data = json.load(auth_json)

    #     for user in authorized_users_data:
    #         authorized_user_data_master.append(user['username'])

    # if username_sign_up in authorized_user_data_master:
    #     return False

    # non_empty_check = non_empty_str_check(username_sign_up)

    # if non_empty_check == False:
    #     return None
    # return True



def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    alldoc = collection.find_one({'Email':email_forgot_passwd}, {'Username':1,'_id':0})

    if alldoc!=None:   
        total = alldoc['Username']
        print(total) 
        return total   
    else:
        return False
    # with open("secret_auth.json", "r") as auth_json:
    #     authorized_users_data = json.load(auth_json)

    #     for user in authorized_users_data:
    #         if user['email'] == email_forgot_passwd:
    #                 return True, user['username']
    # return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def welcome_message(auth_token: str,email_person:str, username: str,company_name: str) -> None:
    """
    Triggers an email to the user welcoming to the site.
    """
    client = Courier(auth_token = auth_token)

    resp = client.send_message(
    message={
        "to": {
        "email": email_person
        },
        "content": {
        "title": company_name,
        "body": "Hi! " + username+ "," + "\n" + "\n" + "Welcome to the Carbon footprint Calculator " + "\n" + "\n" + "{{info}}"
        },
        "data":{
        "info": "Your Account has been sucessfully created. Now, please return to the site to continue filling up details."
        }
    }
    )

def send_passwd_in_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str, random_password: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(auth_token = auth_token)

    resp = client.send_message(
    message={
        "to": {
        "email": email_forgot_passwd
        },
        "content": {
        "title": company_name + ": Login Password!",
        "body": "Hi! " + username_forgot_passwd + "," + "\n" + "\n" + "Your temporary login password is: " + random_password  + "\n" + "\n" + "{{info}}"
        },
        "data":{
        "info": "Please reset your password at the earliest for security reasons."
        }
    }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    collection.update_one({'Email':email_},{'$set': {"Password": random_password}})



def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when
    resetting the password.
    """
    alldoc = collection.find_one({'Email': email_reset_passwd ,'Password': current_passwd },{'Password':1,'_id':0})
    

    try:
        
        if alldoc != None:
            if alldoc["Password"] == current_passwd:
                return True
    except:
        pass
    return False
