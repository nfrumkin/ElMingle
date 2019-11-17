import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('/Users/quentinlin/Google_cloud_cert/round-music-259219-a56a4ede5f89.json')
firebase_admin.initialize_app(cred)

db = firestore.client()



users_db = db.collection(u'user_profiles')
docs = users_db.stream()

# for doc in docs:
# 	db.collection(u'user_profiles').document(doc.id).delete()
# 	# print(u'{} => {}'.format(doc.id, doc.to_dict()))


data = {
    u'name': u'Norman',
    u'online': u'1',
    u'match': u'0',
    u'characterstics': u'mad,user,Google,love,document,id,app'
}

users_db.document('2512835337').set(data)
