import streamlit as st
import pyrebase

#header
st.set_page_config(page_title="Sign Up", layout="centered", page_icon="favicon.ico")

firebaseConfig = {
    'apiKey': "AIzaSyD8HJNlQKPdR-EDzEECLK0l6nLnzvPO-cA",
    'authDomain': "bookai-7cf88.firebaseapp.com",
    'projectId': "bookai-7cf88",
    'databaseURL': "https://YOUR_PROJECT_ID.firebaseio.com",
    'storageBucket': "bookai-7cf88.appspot.com",
    'messagingSenderId': "66262934709",
    'appId': "1:66262934709:web:8c5f3e24ff9d3655c14afc",
    'measurementId': "G-8TNQKF4FNG"
}

# Firebase initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# CSS for styling
def singup_css():
    style = """
        <style>
            .st-emotion-cache-bm2z3a { background-color: #CBDFDC; position: fixed} /*สีพื้นหลัง*/
            .st-emotion-cache-uef7qa { color: #ffeece; } /* สีข้อความในฟิลด์ input */
            .st-b7 { background-color: #ffeece; } 
            .st-cc { border-bottom: 2px solid #f4e0b6; } /*ขอบinputตอนกด*/
            .st-cb { border-top: 2px solid #f4e0b6; } /*ขอบinputตอนกด*/
            .st-ca { border-right: 2px solid #f4e0b6; } /*ขอบinputตอนกด*/
            .st-c9 { border-left: 2px solid #f4e0b6; } /*ขอบinputตอนกด*/
            .st-emotion-cache-12fmjuu { background-color: #CBDFDC; }
            .st-emotion-cache-1wmy9hl { background-color: #fff; border-radius: 20px; margin:0 40px 20px 40px;} /*สีพื้นหลังกรอบด้านใน*/
            .st-emotion-cache-1vt4y43 { border: 0px; } /*ขอบปุ่ม*/
            .stText { color: #333366; }
            .stButton>button { background-color: #ee9fa7; color: #000; } /*ปุ่ม*/
            .stButton>button:hover { box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; background-color: #ee9fa7; color: #000; } /*ปุ่ม*/
            footer { visibility: hidden; }
            #MainMenu { visibility: hidden; }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Sign Up function
def sign_up():
    singup_css()  
    
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
                user = auth.create_user_with_email_and_password(email, password)
                st.session_state.signup_status = "success"
            except Exception as e:
                error_message = str(e)
                if "EMAIL_EXISTS" in error_message:
                    st.error("อีเมลนี้มีบัญชีอยู่แล้ว กรุณาเข้าสู่ระบบแทน")
                else:
                    st.error(f"Sign Up ไม่สำเร็จ: {error_message}")

        # Success message and redirect
        if st.session_state.signup_status == "success":
            st.success("Sign Up สำเร็จ! กรุณาเข้าสู่ระบบ.")
            st.session_state.current_page = "login"
            st.switch_page("pages/login.py")
            st.stop()  # Stop processing to prevent refresh

# Run the app
if __name__ == "__main__":
    sign_up()