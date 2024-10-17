import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
from datetime import timedelta

# Firebase Configuration
cred = credentials.Certificate('bookai-7cf88-firebase-adminsdk-a4x7v-ea828c76b1.json')  # path to your service account key


# Set page configuration
st.set_page_config(page_title="Book Collection", page_icon="favicon.ico")

# Function to display user's book images
def display_books(user_uid):
    st.header("My Books")
    st.write(f"User UID: {user_uid}")
    bucket = storage.bucket()  # Access the storage bucket

    with st.spinner("Loading your books..."):
        try:
            # Specify the path to the user's folder
            user_folder = f"{user_uid}/"  # Path to the user's folder
            blobs = bucket.list_blobs(prefix=user_folder)  # List all files in the user's folder
            
            user_books = [blob for blob in blobs if blob.name.startswith(user_folder)]

            if user_books:
                for book in user_books:
                    # สร้าง URL ที่มีอายุ 15 นาที
                    url = book.generate_signed_url(timedelta(minutes=15))
                    # แสดงภาพ
                    st.image(url, caption=book.name, use_column_width=True)
            else:
                st.write("No books found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Main function to run the app
def main():
    if 'user_uid' in st.session_state and st.session_state.user_uid:
        user_uid = st.session_state.user_uid
        display_books(user_uid)
    else:
        st.write("User not logged in.")

# Run the app
if __name__ == "__main__":
    main()
