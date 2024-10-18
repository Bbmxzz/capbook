import streamlit as st
import easyocr
from roboflow import Roboflow
from PIL import Image, UnidentifiedImageError
import os
import tempfile
from firebase_config import db, bucket
import numpy as np
from pythainlp import word_tokenize

# Initialize Roboflow
rf = Roboflow(api_key="GjIhJ9A525bYsGiVQIRA")
project = rf.workspace("kwsr").project("book-gtby9")
model = project.version(6).model
reader = easyocr.Reader(['th', 'en'])

# Function to read the correction file
def read_correction_file(file_path):
    corrections = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            wrong, right = line.strip().split(',')
            corrections[wrong] = right
    return corrections

# Function to correct book title using corrections from the file
def correct_book_title(book_title, corrections):
    tokens = word_tokenize(book_title, engine='newmm')  # Tokenize the book title
    corrected_title = []
    
    for token in tokens:
        if token in corrections:
            corrected_title.append(corrections[token])  # Use the correct word
        else:
            corrected_title.append(token)  # Use the original word if no correction is found

    return "".join(corrected_title)

# Function to display user's books
def display_books(email):
    try:
        images_ref = db.collection("uploads").document(email).collection("book").stream()
        if st.button("search"):
            st.session_state.current_page = "search"  # Change to search page
            st.switch_page("pages/search.py")

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
                    # Convert file to image
                    image = Image.open(temp_file_path).convert("RGB")  # Convert to RGB
                    st.image(image, caption="ภาพที่อัพโหลด", use_column_width=True)

                    # Process the image to find the regions to read with Roboflow
                    with st.spinner("กำลังตรวจจับตำแหน่งชื่อหนังสือ..."):
                        predictions = model.predict(temp_file_path, confidence=40, overlap=30).json()

                        if predictions['predictions']:
                            # Show detected positions
                            for pred in predictions['predictions']:
                                st.image(image.crop(( 
                                    pred['x'] - (pred['width']/2),
                                    pred['y'] - (pred['height']/2),
                                    pred['x'] + (pred['width']/2),
                                    pred['y'] + (pred['height']/2)
                                )), caption="ตำแหน่งชื่อหนังสือ", use_column_width=True)

                            # Read book title from the detected positions
                            book_title = ""
                            for pred in predictions['predictions']:
                                # Crop image to the bounding box of the prediction
                                cropped_image = image.crop(( 
                                    pred['x'] - (pred['width']/2),
                                    pred['y'] - (pred['height']/2),
                                    pred['x'] + (pred['width']/2),
                                    pred['y'] + (pred['height']/2)
                                )).convert('L')
                                
                                # Read book title using EasyOCR
                                result = reader.readtext(np.array(cropped_image), detail=0, paragraph=True)
                                if result:
                                    book_title += " ".join(result) + " "  # Combine the recognized titles

                            if book_title.strip():
                                st.write(f"ชื่อหนังสือก่อนแก้ไข: {book_title.strip()}")
                                
                                # อ่านไฟล์ correction.txt
                                corrections = read_correction_file('corrections.txt')  # เส้นทางไฟล์อาจจะต้องปรับตามที่เก็บ
                                
                                # แก้ไขชื่อหนังสือ
                                corrected_title = correct_book_title(book_title, corrections)
                                
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
                                    st.write(f"Public URL: {image_url}")

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
                        else:
                            st.write("ไม่พบตำแหน่งชื่อหนังสือในภาพ.")
                except UnidentifiedImageError:
                    st.error("ไม่สามารถเปิดไฟล์ภาพที่ถูกบันทึกชั่วคราวได้. โปรดตรวจสอบว่าเป็นรูปภาพที่ถูกต้อง.")
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
