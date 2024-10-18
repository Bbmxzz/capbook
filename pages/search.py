import streamlit as st
import easyocr
from roboflow import Roboflow
from PIL import Image, UnidentifiedImageError
import os
import tempfile
from firebase_config import db, bucket
import numpy as np

rf = Roboflow(api_key="GjIhJ9A525bYsGiVQIRA")
project = rf.workspace("kwsr").project("book-gtby9")
model = project.version(6).model
reader = easyocr.Reader(['th', 'en'])

def search_book_page(email):
    if st.button("homepage"):
        st.session_state.page = "mybook"  # Set a session state variable
        st.switch_page("pages/mybook.py")
    st.title("ค้นหาหนังสือ")

    # File upload for searching
    search_file = st.file_uploader("อัพโหลดรูปภาพหนังสือเพื่อค้นหา", type=["jpg", "jpeg", "png"])

    if search_file is not None:
        try:
            search_file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(search_file.read())
                temp_file_path = temp_file.name

            if os.path.exists(temp_file_path):
                image = Image.open(temp_file_path).convert("RGB")
                st.image(image, caption="ภาพที่อัพโหลดเพื่อค้นหา", use_column_width=True)

                # Process the image to find the regions to read with Roboflow
                with st.spinner("กำลังตรวจจับตำแหน่งชื่อหนังสือ..."):
                    predictions = model.predict(temp_file_path, confidence=40, overlap=30).json()

                    if predictions['predictions']:
                        book_title = ""
                        for pred in predictions['predictions']:
                            cropped_image = image.crop(( 
                                pred['x'] - (pred['width']/2),
                                pred['y'] - (pred['height']/2),
                                pred['x'] + (pred['width']/2),
                                pred['y'] + (pred['height']/2)
                            )).convert('L')
                            
                            result = reader.readtext(np.array(cropped_image), detail=0, paragraph=True)
                            if result:
                                book_title += " ".join(result) + " "

                        if book_title.strip():
                            st.write(f"ชื่อหนังสือที่ค้นพบ: {book_title.strip()}")

                            # Check Firestore for the book
                            email = st.session_state.email
                            images_ref = db.collection("uploads").document(email).collection("book").stream()
                            found = False
                            for image_doc in images_ref:
                                image_data = image_doc.to_dict()
                                if book_title.strip() in image_data.get('namebook', ''):
                                    st.image(image_data['image_url'], caption=image_data.get('namebook', ''))
                                    found = True
                            
                            if not found:
                                st.write("ไม่พบหนังสือในระบบ.")

                        else:
                            st.write("ไม่สามารถอ่านชื่อหนังสือจากภาพได้.")
                    else:
                        st.write("ไม่พบตำแหน่งชื่อหนังสือในภาพ.")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    
            
def main():
    st.title("ระบบจัดการหนังสือ")

    if 'email' in st.session_state and st.session_state.email:
        email = st.session_state.email
        st.write("---")
        search_book_page(email)  # Call the search book function
        
    else:
        st.write("ผู้ใช้ยังไม่ได้เข้าสู่ระบบ.")

# Run the app
if __name__ == "__main__":
    main()