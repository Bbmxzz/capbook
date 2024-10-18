import firebase_admin
from firebase_admin import credentials, firestore, storage


if not firebase_admin._apps:
    cred = credentials.Certificate("bookai-7cf88-firebase-adminsdk-a4x7v-6ddad91682.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'bookai-7cf88.appspot.com'  # เพิ่มชื่อ bucket ตรงนี้
    })

db = firestore.client()

# เข้าถึง Firebase Storage
bucket = storage.bucket()