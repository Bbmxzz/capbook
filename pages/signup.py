import streamlit as st
from firebase_config import db

# Header
st.set_page_config(page_title="Sign Up", layout="centered", page_icon="favicon.ico")

# CSS for styling
def signup_css():
    style = """
        <style>
            .st-emotion-cache-bm2z3a { background-color: #CBDFDC; }
            .st-emotion-cache-uef7qa { color: #ffeece; }
            .st-b7 { background-color: #ffeece; } 
            .st-cc { border-bottom: 2px solid #f4e0b6; }
            .st-cb { border-top: 2px solid #f4e0b6; }
            .st-ca { border-right: 2px solid #f4e0b6; }
            .st-c9 { border-left: 2px solid #f4e0b6; }
            .st-emotion-cache-12fmjuu { background-color: #CBDFDC; }
            .st-emotion-cache-1n76uvr{ padding: 0 40px 20px 40px; }
            .st-emotion-cache-1wmy9hl { 
                background-color: #fff; 
                border-radius: 20px; 
                margin: 0 70px;} 
            .st-emotion-cache-1vt4y43 { border: 0px; }
            .stText { color: #333366; }

            .input-container {
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid #f4e0b6;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 20px;
                background-color: #ffeece;
                width: 50%;  /* ปรับขนาดช่องกรอกข้อมูล */
                margin: auto;  /* จัดให้อยู่ตรงกลาง */
            }
            .icon {
                margin-right: 10px;  /* ระยะห่างระหว่างไอคอนและช่องกรอกข้อมูล */
                margin-left: 17px;
                margin-top: 36px;
                fill: rgba(0, 0, 0, 1);
            }
            footer { visibility: hidden; }
            #MainMenu { visibility: hidden; }
            h1 {
                text-align: center;
                color: #333366;
            }
            .stButton>button {
                background-color: #ee9fa7;
                color: #000;
                font-weight: bold;
                font-size: 16px;
                border-radius: 15px;
                padding: 10px;
                width: 25%;
                margin-top: 20px;
                margin-left: auto;
                margin-right: auto;
                display: block;
                cursor: pointer;
                border: none;
            }
            .stButton>button:hover {
                box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
                color: #000;
            }
            /* Center alignment for login link */
            .signup-link {
                text-align: center;
                margin-top: 10px;
                margin-bottom: 40px;
                font-size: 17px;
            }
            .signup-link a {
                color: #ff0066;
                text-decoration: none;
                font-weight: bold;
            }
            .signup-link a:hover {
                color: #000;
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Sign Up function
def sign_up():
    signup_css()  
    
    st.title("Sign Up")
    st.write("")  # Add space

    # Input fields with SVG icons in separate columns
    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown("""
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M7.5 6.5C7.5 8.981 9.519 11 12 11s4.5-2.019 4.5-4.5S14.481 2 12 2 7.5 4.019 7.5 6.5zM20 21h1v-1c0-3.859-3.141-7-7-7h-4c-3.86 0-7 3.141-7 7v1h17z"></path></svg>
        """, unsafe_allow_html=True)
    with col2:
        username = st.text_input("Username", placeholder="Username")

    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown("""
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.7-8 5.334L4 8.7V6.297l8 5.333 8-5.333V8.7z"></path></svg>
        """, unsafe_allow_html=True)
    with col2:
        email = st.text_input("Email", placeholder="example@gmail.com")

    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown("""
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 2C9.243 2 7 4.243 7 7v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V7c0-2.757-2.243-5-5-5zM9 7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9V7zm4 10.723V20h-2v-2.277a1.993 1.993 0 0 1 .567-3.677A2.001 2.001 0 0 1 14 16a1.99 1.99 0 0 1-1 1.723z"></path></svg>
        """, unsafe_allow_html=True)
    with col2:
        password = st.text_input("Password", type="password", placeholder="Password")

    # Sign Up button logic
    if st.button("Sign Up"):
        try:
            # Check if the email already exists
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
    st.markdown('<div class="signup-link">Already have an account? <a href="login">Login</a></div>', unsafe_allow_html=True)

    # Add functionality to switch to login page when the link is clicked
    if st.session_state.get("current_page") == "login":
        st.switch_page("pages/login.py")
    st.write("")


# Run the app
if __name__ == "__main__":
    sign_up()
