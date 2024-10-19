import streamlit as st
from firebase_config import db

def login_css():
    style = """
        <style>
            /* Your CSS styling here */
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
                margin: 0 30px;} 
            .st-emotion-cache-1vt4y43 { border: 0px; }
            .stText { color: #333366; }
            .stButton>button {
                background-color: #ee9fa7;
                color: #000; 
                border-radius: 5px; 
                padding: 10px; 
                width: 100%; 
                cursor: pointer; 
                border: none; 
            }
            .stButton>button:hover {
                box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; 
                color: #000;
            }
            footer { visibility: hidden; }
            #MainMenu { visibility: hidden; }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

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
                # Check if the user exists in Firestore
                user_ref = db.collection("users").where("email", "==", email).limit(1).get()

                if len(user_ref) == 0:
                    st.error("No account found with this email.")
                else:
                    user = user_ref[0].to_dict()  # Get the user data
                    stored_password = user.get("password")  # Get stored password
                     
                    # ตรวจสอบรหัสผ่าน
                    if stored_password and stored_password == password:
                        st.session_state.email = email  # Store user UID
                        st.session_state.login_status = "success"
                        st.success("Login successful!")
                        st.session_state.current_page = "mybook"  # Change to Home page
                        st.switch_page("pages/mybook.py")
                    else:
                        st.error("Incorrect password.")

            except Exception as e:
                st.error("Login failed. Please check your credentials.")
        st.write("")

if __name__ == "__main__":
    login()
