import firebase_admin
from firebase_admin import credentials, storage


cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://eco-reporte.appspot.com'
})
