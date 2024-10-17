import streamlit as st
import pyrebase

# Header
st.set_page_config(page_title="Sign Up", layout="centered", page_icon="favicon.ico")

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
db = firebase.database()  # Initialize the database

# CSS for styling
def signup_css():
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

# Sign Up function
def sign_up():
    signup_css()  
    
    # Create a container for centering content
    with st.container():
        st.title("Sign Up")
        st.write("")  # Add space
        
        # Initialize session state for signup status
        if "signup_status" not in st.session_state:
            st.session_state.signup_status = None

        # Input fields
        username = st.text_input("Username", placeholder="Username")
        email = st.text_input("Email", placeholder="example@gmail.com")
        password = st.text_input("Password", type="password", placeholder="Password")

        # Sign Up button logic
        if st.button("Sign Up"):
            try:
                # Create user in Firebase Authentication
                user = auth.create_user_with_email_and_password(email, password)
                st.session_state.signup_status = "success"

                # Save user data in Firestore
                user_id = user['localId']  # Get user ID
                db.child("users").child(user_id).set({
                    "username": username,
                    "email": email,
                })

            except Exception as e:
                error_message = str(e)
                if "EMAIL_EXISTS" in error_message:
                    st.error("This email already has an account, please log in instead.")
                else:
                    st.error(f"Sign Up failed: {error_message}")

        # Success message and redirect
        if st.session_state.signup_status == "success":
            st.success("Sign Up successful! Please log in.")
            st.session_state.current_page = "login"
            st.switch_page("pages/login.py")
            st.stop()  # Stop processing to prevent refresh
        st.write("")


# Run the app
if __name__ == "__main__":
    sign_up()
