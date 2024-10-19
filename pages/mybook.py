import streamlit as st
import os
import tempfile
from firebase_config import db, bucket
from process import process_book_image, model
# Header
st.set_page_config(page_title="My book", layout="centered", page_icon="favicon.ico")

def display_books(email):
    try:
        images_ref = db.collection("uploads").document(email).collection("book").stream()
        if st.button("search"):
            st.session_state.current_page = "search"  # Change to search page
            st.switch_page("pages/search.py")
        if st.button("Logout"):
            st.session_state.email = None
            st.session_state.current_page = "login"  # Change to search page
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
                st.write("ไม่พบรูปภาพในระบบ.")
        else:
            st.write("ไม่พบรูปภาพในระบบ.")

    except Exception as e:
        st.write(f"เกิดข้อผิดพลาด: {e}")

def add_book_page():
    st.title("เพิ่มหนังสือใหม่")

    # File upload
    uploaded_file = st.file_uploader("อัพโหลดรูปภาพหนังสือ", type=["jpg", "jpeg", "png"])

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
                    with st.spinner("กำลังตรวจจับตำแหน่งชื่อหนังสือ..."):
                        corrected_title = process_book_image(temp_file_path, model)

                        if corrected_title:
                            st.write(f"ชื่อหนังสือหลังแก้ไข: {corrected_title.strip()}")

                            # แสดงปุ่ม "เพิ่มหนังสือ" หลังจากอ่านชื่อเรียบร้อยแล้ว
                            if st.button("เพิ่มหนังสือ"):
                                uploaded_file.seek(0)
                                email = st.session_state.email
                                folder_path = f"{email}/{uploaded_file.name}"  # สร้างเส้นทางที่มีชื่อเป็นอีเมลของผู้ใช้
                                blob = bucket.blob(folder_path)  # อัปโหลดไฟล์ไปที่โฟลเดอร์ email ของผู้ใช้
                                blob.upload_from_file(uploaded_file, content_type='image/jpeg')
                                blob.make_public()  # ทำให้ไฟล์เป็นสาธารณะ
                                image_url = blob.public_url  # รับ URL สาธารณะของภาพ

                                # บันทึกรายละเอียดหนังสือไปยัง Firestore
                                db.collection("uploads").document(email).collection("book").add({
                                    "namebook": corrected_title.strip(),
                                    "image_url": image_url  # URL of the uploaded image
                                })
                                st.success("เพิ่มหนังสือเรียบร้อยแล้ว!")
                                uploaded_file = None
                                st.switch_page("pages/mybook.py")
                        else:
                            st.write("ไม่สามารถอ่านชื่อหนังสือจากภาพได้.")
                            st.session_state.current_page = "mybook"  # Change to Home page
                            st.switch_page("pages/mybook.py")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.error("ไฟล์ชั่วคราวไม่พบ.")
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

# Main function to display in the app
def main():
    st.title("ระบบจัดการหนังสือ")

    if 'email' in st.session_state and st.session_state.email:
        email = st.session_state.email
        display_books(email)  # Show existing books
        st.write("---")
        add_book_page()  # Call the add book function
    else:
        st.write("ผู้ใช้ยังไม่ได้เข้าสู่ระบบ.")

# Run the app
if __name__ == "__main__":
    main()
