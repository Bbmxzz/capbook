import streamlit as st
import os
import tempfile
from firebase_config import db, bucket
from process import process_book_image, model

# Header
st.set_page_config(page_title="Search", layout="centered", page_icon="favicon.ico")

def search_book_page(email):
    st.title("Search for a Book")

    st.markdown("<h4 style='font-size: 18px; color: #333366'>Upload a book image to search </h4>", unsafe_allow_html=True)

    # File upload
    search_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    # search_file = st.file_uploader("Upload a book image to search", type=["jpg", "jpeg", "png"])

    if search_file is not None:
        try:
            search_file.seek(0)
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(search_file.read())
                temp_file_path = temp_file.name

            # Check if the temporary file exists and is valid
            if os.path.exists(temp_file_path):
                with st.spinner("Searching for the book..."):
                    # Process the uploaded image
                    corrected_title = process_book_image(temp_file_path, model)

                    if corrected_title:
                        # Check Firestore for the book
                        images_ref = db.collection("uploads").document(email).collection("book").stream()
                        found = False
                        for image_doc in images_ref:
                            image_data = image_doc.to_dict()
                            if corrected_title.strip() in image_data.get('namebook', ''):
                                st.write(f"Found Book: {corrected_title.strip()}")
                                st.image(image_data['image_url'], caption=image_data.get('namebook', ''))
                                found = True
                                break  # Stop searching once we find the book

                        if not found:
                            st.write("No books found or data passed incorrectly.")
                    else:
                        st.write("Unable to read the book title from the image.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def main():
    st.title("CapBook Management System")

    col1, col2 = st.columns([7, 1])
    with col1:
        if st.button(" < Back to Mybook"):
            st.session_state.current_page = "mybook"  # Change to search page
            st.switch_page("pages/mybook.py")
    with col2:
        if st.button("Logout"):
            st.session_state.email = None
            st.session_state.current_page = "login"  # Change to login page
            st.switch_page("pages/login.py")

    if 'email' in st.session_state and st.session_state.email:
        email = st.session_state.email
        st.write("---")
        search_book_page(email)  # Call the search book function
        
    else:
        st.write("User is not logged in.")

# Run the app
if __name__ == "__main__":
    main()
