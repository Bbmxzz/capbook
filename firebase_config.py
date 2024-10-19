import firebase_admin
from firebase_admin import credentials, firestore, storage
import os


if not firebase_admin._apps:
    
    cred = credentials.Certificate({
    "type": os.getenv("type"),
    "project_id": os.getenv("project_id"),
    "private_key_id": os.getenv("private_key_id"),
    "private_key": os.getenv("private_key").replace('\\n', '\n'),  # Replace escaped newlines
    "client_email": os.getenv("client_email"),
    "client_id": os.getenv("client_id"),
    "auth_uri": os.getenv("auth_uri"),
    "token_uri": os.getenv("token_uri"),
    "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.getenv("client_x509_cert_url")
})
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'bookai-7cf88.appspot.com'  # เพิ่มชื่อ bucket ตรงนี้
    })

db = firestore.client()

# เข้าถึง Firebase Storage
bucket = storage.bucket()