import streamlit as st
from firebase_config import db

# Header
st.set_page_config(page_title="Sign Up", layout="centered", page_icon="favicon.ico")

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
            .st-emotion-cache-1n76uvr {
                padding: 0 40px 20px 40px; 
            }
            .st-emotion-cache-1wmy9hl { 
                background-color: #fff; 
                border-radius: 20px; 
                margin: 0 30px;
            } /* Inner frame background color */
                
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
    
    with st.container():
        st.title("Sign Up")
        st.write("")  # Add space
        
        # Input fields
        username = st.text_input("Username", placeholder="Username")
        email = st.text_input("Email", placeholder="example@gmail.com")
        password = st.text_input("Password", type="password", placeholder="Password")

        # Sign Up button logic
        if st.button("Sign Up"):
            try:
                # Save user data in Firestore
                user_data = {
                    "username": username,
                    "email": email,
                    "password": password  # แนะนำให้เก็บรหัสผ่านในรูปแบบที่เข้ารหัส
                }
                
                # Check if the email already exists
                existing_users = db.collection("users").where("email", "==", email).get()
                if existing_users:
                    st.error("This email already has an account, please log in instead.")
                else:
                    # Save user data in Firestore
                    db.collection("users").document(email).set(user_data)
                    st.session_state.current_page = "login"  # Change to Home page
                    st.switch_page("pages/login.py")
                    st.success("Sign Up successful! Please log in.")
    
            except Exception as e:
                st.error(f"Sign Up failed: {str(e)}")
        st.write("")
        st.markdown("If you already have an account, [click here to log in](login).", unsafe_allow_html=True)

        # Add functionality to switch to login page when the link is clicked
        if st.session_state.get("current_page") == "login":
            st.switch_page("pages/login.py")
        st.write("")

# Run the app
if __name__ == "__main__":
    sign_up()
