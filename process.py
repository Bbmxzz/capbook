import easyocr
import numpy as np
from PIL import Image
from pythainlp import word_tokenize
from roboflow import Roboflow
import streamlit as st

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


def process_book_image(image_path, model):
    try:
        # Open and convert image to RGB
        image = Image.open(image_path).convert("RGB")
        st.image(image, caption="รูปภาพที่อัพโหลด", use_column_width=True)

        # Use Roboflow model to predict the positions of book titles
        predictions = model.predict(image_path, confidence=40, overlap=30).json()

        if predictions['predictions']:
            book_title = ""
            for pred in predictions['predictions']:
                # Crop the image based on the prediction bounding box
                cropped_image = image.crop((
                    pred['x'] - (pred['width'] / 2),
                    pred['y'] - (pred['height'] / 2),
                    pred['x'] + (pred['width'] / 2),
                    pred['y'] + (pred['height'] / 2)
                )).convert('L')

                # Use EasyOCR to read the text from the cropped image
                result = reader.readtext(np.array(cropped_image), detail=0, paragraph=True)
                if result:
                    book_title += " ".join(result) + " "  # Combine recognized texts

            # If book title is found, correct it using corrections.txt
            if book_title.strip():
                corrections = read_correction_file('corrections.txt')  # Path to corrections file may vary
                corrected_title = correct_book_title(book_title, corrections)
                return corrected_title.strip()
            else:
                return None
        else:
            return None

    except Exception as e:
        raise Exception(f"Error processing image: {e}")
