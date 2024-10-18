import numpy as np
import easyocr
import pandas as pd
import os
import re
from roboflow import Roboflow
from PIL import Image

# Initialize Roboflow client
rf = Roboflow(api_key="GjIhJ9A525bYsGiVQIRA")
project = rf.workspace("kwsr").project("book-gtby9")
model = project.version(6).model
reader = easyocr.Reader(['th', 'en'])

def read_name_from_image(image_path):
    result = model.predict(image_path).json()
    
    detected_names = []
    bounding_boxes = []
    
    if 'predictions' in result:
        for prediction in result['predictions']:
            name = prediction['class']
            x1 = int(prediction['x'] - prediction['width'] / 2)
            y1 = int(prediction['y'] - prediction['height'] / 2)
            x2 = int(prediction['x'] + prediction['width'] / 2)
            y2 = int(prediction['y'] + prediction['height'] / 2)
            
            detected_names.append(name)
            bounding_boxes.append((x1, y1, x2, y2))

    return detected_names, bounding_boxes

def crop_and_read_names(image_path, bounding_boxes):
    image = Image.open(image_path)
    cropped_names = []

    for box in bounding_boxes:
        x1, y1, x2, y2 = box
        cropped_image = np.array(image)[y1:y2, x1:x2]
        
        result = reader.readtext(cropped_image)
        for (_, text, _) in result:
            cleaned_text = re.sub(r'\s+', '', text)
            cropped_names.append(cleaned_text.strip())

    return cropped_names


