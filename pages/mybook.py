import streamlit as st
import os
import tempfile
from firebase_config import db, bucket
from process import process_book_image, model

# Header
st.set_page_config(page_title="My Book", layout="centered", page_icon="favicon.ico")

def display_books(email):
    try:
        images_ref = db.collection("uploads").document(email).collection("book").stream()
        
        # Create two columns for Search and Logout buttons
        col1, col2 = st.columns([7, 1])
        with col1:
            # Detect click event in Streamlit for switching to search page
            if st.button("Search"):
                st.session_state.current_page = "search"  # Change to search page
                st.switch_page("pages/search.py")

        with col2:
            if st.button("Logout"):
                st.session_state.email = None
                st.session_state.current_page = "login"  # Change to login page
                st.switch_page("pages/login.py")

        if images_ref:
            cols = st.columns(3)  # Create 3 columns for grid layout
            index = 0
            for image in images_ref:
                image_data = image.to_dict()
                if 'image_url' in image_data:
                    image_url = image_data['image_url']

                    # Display the image in the appropriate column
                    with cols[index % 3]:  # Use modulo to cycle through columns
                        st.image(image_url, caption=image_data.get('namebook', ''), use_column_width='always')
                    
                    index += 1  # Increment the index for the next image

            if index == 0:
                st.write("No images found in the system.")
        else:
            st.write("No images found in the system.")

    except Exception as e:
        st.write(f"An error occurred: {e}")

def add_book_page():
    st.title("Add New Book")

    # ปรับขนาดฟอนต์ของประโยค Upload a book image
    st.markdown("<h4 style='font-size: 18px; color: #333366'>Upload a book image</h4>", unsafe_allow_html=True)

    # File upload
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Check if the temporary file exists and is valid
            if os.path.exists(temp_file_path):
                try:
                    # Process the image to find the book title
                    with st.spinner("Detecting the book title..."):
                        corrected_title = process_book_image(temp_file_path, model)

                        if corrected_title:
                            st.write(f"Corrected Book Title: {corrected_title.strip()}")

                            # Show "Add Book" button after reading the title
                            if st.button("Add Book"):
                                uploaded_file.seek(0)
                                email = st.session_state.email
                                folder_path = f"{email}/{uploaded_file.name}"  # Create a path with the user's email
                                blob = bucket.blob(folder_path)  # Upload the file to the user's folder
                                blob.upload_from_file(uploaded_file, content_type='image/jpeg')
                                blob.make_public()  # Make the file public
                                image_url = blob.public_url  # Get the public URL of the image

                                # Save book details to Firestore
                                db.collection("uploads").document(email).collection("book").add({
                                    "namebook": corrected_title.strip(),
                                    "image_url": image_url  # URL of the uploaded image
                                })
                                st.success("Book added successfully!")
                                st.write("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)
                                st.switch_page("pages/mybook.py")
                                
                                
                        else:
                            st.write("Unable to read the book title from the image.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Temporary file not found.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Main function to display in the app
def main():
    st.title("CapBook Management System")

    if 'email' in st.session_state and st.session_state.email:
        email = st.session_state.email
        display_books(email)  # Show existing books
        st.write("---")
        add_book_page()  # Call the add book function
    else:
        st.write("User is not logged in.")

# Run the app
if __name__ == "__main__":
    main()
