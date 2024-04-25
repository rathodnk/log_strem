import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import re
import subprocess

load_dotenv()

client = MongoClient(os.getenv('mdb'))

db = client['DB1']
collection = db['IDs']

def login():
    st.title("FoodInfo using Image")
    st.write("This is a paltform where you can share the thoughs.")
    st.write("Please login to continue.")

    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
        # Check if username and password match
            user = collection.find_one({"username": username, "password": password})
            if user:
                st.success("Login successful!")
                st.session_state.logged_in = True
                 # Call main_app.py upon successful login
                subprocess.Popen(["streamlit", "run", "app.py"])
            else:
                st.error("Invalid username or password.")

    st.markdown('<center>If you New then <a href="http://localhost:8501/?page=signup" target="_self">Sign Up!</a></center>', unsafe_allow_html=True)
    

def signup():
    def passwrd_valid(password):
        # Regular expression to check if the password meets the criteria
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$"
        if re.match(regex, password):
            return True
        else:
            return False

    st.header('FoodInfo Sign Up')

    with st.form(key = "register_form"):
        name = st.text_input("Name", max_chars=50)
        username = st.text_input("Username", max_chars=16)
        password = st.text_input("Password", type="password", max_chars=16)
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Register"):
            # Check if all fields are filled
            if not name or not username or not password or not confirm_password:
                st.warning("Please fill in all fields")
                st.stop()

            if name.replace(" ","").isalpha() == False:
                st.warning("Name should be Alphabet")
                st.stop()

            if username.isalnum() == False:
                st.warning("Username should be Alphanumeric")
                st.stop()

            if passwrd_valid(password) == False:
                st.error("Password should contains Upper, Lower, Numbers and Symbols. Length 8 to 16.")
                st.stop()

            # Password confirmation
            if password != confirm_password:
                st.error("The passwords do not match")
                st.stop()

            # Check if username already exists
            existing_user = collection.find_one({"username": username})
            if existing_user:
                st.error("Username already exists. Please choose a different one.")
            else:
                # Insert new user into the database
                user_data = {"name": name.title(), "username": username, "password": password}
                collection.insert_one(user_data)
                st.success("User registered successfully! Go back to LogIN")
                st.balloons()

    st.markdown('<a href="http://localhost:8501/?page=login" target="_self">Back to Login</a>', unsafe_allow_html=True)

def main():
    page = st.query_params.get("page", "login")
    if page == "login":
        login()
    elif page == "signup":
        signup()

if __name__ == "__main__":
    main()


client.close()






