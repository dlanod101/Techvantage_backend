import firebase_admin
from firebase_admin import credentials, auth

# Use the path to your service account JSON file
cred = credentials.Certificate(

)
firebase_admin.initialize_app(cred)
