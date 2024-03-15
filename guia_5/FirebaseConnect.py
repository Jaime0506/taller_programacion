import firebase_admin
import os
from firebase_admin import credentials, db

key_path = os.path.join(os.path.dirname(__file__), 'firebase')
key = os.path.join(key_path, 'space-shooter-9c882-firebase-adminsdk-tndg0-ca7618fd2e.json')

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://space-shooter-9c882-default-rtdb.firebaseio.com/'})

ref = db.reference('/player_1')
ref_ship = ref.child('-Nsz_waZceu5sMSuXRXq')

