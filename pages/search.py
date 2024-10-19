import streamlit as st
import os
import tempfile
from firebase_config import db, bucket
from process import process_book_image, model
# Header
st.set_page_config(page_title="Search", layout="centered", page_icon="favicon.ico")

def search_book_page(email):
    st.title("ค้นหาหนังสือ")

    # ตรวจสอบสถานะว่ามีการอัปโหลดไฟล์หรือไม่
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False  # เริ่มต้นสถานะ

    # File upload for searching
    if not st.session_state.file_uploaded:
        search_file = st.file_uploader("อัพโหลดรูปภาพหนังสือเพื่อค้นหา", type=["jpg", "jpeg", "png"])

        if search_file is not None:
            try:
                search_file.seek(0)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_file.write(search_file.read())
                    temp_file_path = temp_file.name

                if os.path.exists(temp_file_path):
                    with st.spinner("กำลังค้นหาหนังสือ..."):
                        # Process the uploaded image
                        corrected_title = process_book_image(temp_file_path, model)

                        if corrected_title:

                            # Check Firestore for the book
                            images_ref = db.collection("uploads").document(email).collection("book").stream()
                            found = False
                            for image_doc in images_ref:
                                image_data = image_doc.to_dict()
                                if corrected_title.strip() in image_data.get('namebook', ''):
                                    st.write(f"Found Books: {corrected_title.strip()}")
                                    st.image(image_data['image_url'], caption=image_data.get('namebook', ''))
                                    found = True
                                    break  # Stop searching once we find the book
                            
                            if found:
                                st.session_state.file_uploaded = True  # Mark the file as uploaded
                            else:
                                st.write("ไม่พบหนังสือในระบบ.")
                        else:
                            st.write("ไม่สามารถอ่านชื่อหนังสือจากภาพได้.")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.write("คุณได้ค้นหาหนังสือแล้ว.")

    
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
