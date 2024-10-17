import streamlit as st
import pyrebase

def login_css():
    style = """
        <style>
            .st-emotion-cache-bm2z3a { background-color: #CBDFDC; } /* Background color */
            .st-emotion-cache-uef7qa { color: #ffeece; } /* Input field text color */
            .st-b7 { background-color: #ffeece; } 
            .st-cc { border-bottom: 2px solid #f4e0b6; } /* Input border when focused */
            .st-cb { border-top: 2px solid #f4e0b6; } /* Input border when focused */
            .st-ca { border-right: 2px solid #f4e0b6; } /* Input border when focused */
            .st-c9 { border-left: 2px solid #f4e0b6; } /* Input border when focused */
            .st-emotion-cache-12fmjuu { background-color: #CBDFDC; }
            .st-emotion-cache-1n76uvr{
                padding: 0 40px 20px 40px; 
            }
            .st-emotion-cache-1wmy9hl { 
                background-color: #fff; 
                border-radius: 20px; 
                margin: 0 30px;} /* Inner frame background color */
                
            .st-emotion-cache-1vt4y43 { border: 0px; } /* Button border */
            .stText { color: #333366; }
            .stButton>button {
                background-color: #ee9fa7; /* Button color */
                color: #000; /* Button text color */
                border-radius: 5px; /* Rounded corners */
                padding: 10px; /* Internal padding */
                width: 100%; /* Full-width button */
                cursor: pointer; /* Change cursor */
                border: none; /* No border */
            }
            .stButton>button:hover {
                box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; /* Shadow on hover */
                color: #000;
            }
            footer { visibility: hidden; }
            #MainMenu { visibility: hidden; }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Firebase config
firebaseConfig = {
    'apiKey': "AIzaSyD8HJNlQKPdR-EDzEECLK0l6nLnzvPO-cA",
    'authDomain': "bookai-7cf88.firebaseapp.com",
    'projectId': "bookai-7cf88",
    'databaseURL': "https://bookai-7cf88-default-rtdb.firebaseio.com",
    'storageBucket': "bookai-7cf88.appspot.com",
    'messagingSenderId': "66262934709",
    'appId': "1:66262934709:web:8c5f3e24ff9d3655c14afc",
    'measurementId': "G-8TNQKF4FNG"
}

# Firebase initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login():
    login_css()
    
    with st.container():
        st.title("Login")
        if "login_status" not in st.session_state:
            st.session_state.login_status = None  # Default status is None

        email = st.text_input("Email", placeholder="example@gmail.com")
        password = st.text_input("Password", type="password", placeholder="Password")

        if st.button("Login"):
            try:
                # Attempt to sign in the user
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user_uid = user['localId']  # Store user UID
                st.session_state.login_status = "success"
                st.session_state.email = email  # Store email in session state
                st.success("Login successful!")
                st.session_state.current_page = "mybook"  # Change to Home page
                st.switch_page("pages/mybook.py") 
            except Exception as e:
                st.error("Login failed. Please check your credentials.")
        st.write("")

if __name__ == "__main__":
    login()
