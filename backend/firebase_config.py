import firebase_admin
from firebase_admin import credentials, firestore, storage

# Inicializar apenas uma vez
def init_firebase():
    if not firebase_admin._apps:  # Evita inicializar duas vezes
        cred = credentials.Certificate("smartticket-8bd4c-firebase-adminsdk-fbsvc-0c43228df1.json")

        firebase_admin.initialize_app(cred, {
            "projectId": "smartticket-8bd4c",
            "storageBucket": "smartticket-8bd4c.firebasestorage.app"
        })

    return {
        "db": firestore.client(),
        "bucket": storage.bucket()
    }

