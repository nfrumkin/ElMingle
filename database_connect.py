import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('/home/natasha/athena/Desktop/ElMingle/ElMingleCreds.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    u'name': u'Natasha',
    u'intro_url': u'https://nfrumkin.github.io'
}

db.collection(u'user_profiles').document('4083142208').set(data)