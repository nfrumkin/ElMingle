import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('/Users/quentinlin/Google_cloud_cert/round-music-259219-a56a4ede5f89.json')
firebase_admin.initialize_app(cred)

db = firestore.client()



users_db = db.collection(u'user_profiles')
docs = list(users_db.stream())

targetID='4133256695'

#search generator for current call id 
for doc in docs:
	# print(u'{} => {}'.format(doc.id, doc.to_dict()))
	if(targetID==doc.id):
		caller_dict=doc.to_dict()
		caller_char_str = caller_dict.get('characterstics')
		caller_char_list=caller_char_str.split(",")
		break

print("Comparing to")
print(caller_char_list)

i=0
for doc in docs:
	i=i+1
	# print(u'{} => {}'.format(doc.id, doc.to_dict()))
	if(targetID!=doc.id):
		print("Entry %d: Phone#: %s"%(i, doc.id))
		doc_dict=doc.to_dict()
		char_str = doc_dict.get('characterstics')
		charList=char_str.split(",")
		res = len(set(caller_char_list) & set(charList)) / float(len(set(caller_char_list) | set(charList))) * 100
		print("\tName %s, Similarity Score: %d"%(doc_dict.get('name'),  res))
		print(charList)



# print(type(docs ))