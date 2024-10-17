import streamlit as st

st.set_page_config(page_title="My App", page_icon="favicon.ico", layout="centered")

# ตั้งค่าหน้าเริ่มต้นของ Streamlit
if "current_page" not in st.session_state:
    st.session_state.current_page = "sign_up"

# ตรวจสอบว่าเป็นหน้า sign_up หรือไม่
if st.session_state.current_page == "sign_up":
    ShowSidebarNavigation = False

def main():
    # ตรวจสอบสถานะของ current_page และเรียก switch_page ตามหน้า
    if st.session_state.current_page == "login":
        st.switch_page("pages/login.py")  # ไปที่หน้า Login
    if st.session_state.current_page == "sign_up":
        st.switch_page("pages/signup.py")  # ไปที่หน้า Sign Up
    elif st.session_state.current_page == "mybook":
        st.switch_page("pages/mybook.py")  # ไปที่หน้า Chatbot

if __name__ == "__main__":
    main()