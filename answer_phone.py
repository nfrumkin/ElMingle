from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Record, Dial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


app = Flask(__name__)

recordingURL = ""
MODERATOR = '+12034875958'

# Use a service account
cred = credentials.Certificate('/home/natasha/athena/Desktop/ElMingle/ElMingleCreds.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
client = speech.SpeechClient()

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    userNumber = request.values.get('From')

    # Start our TwiML response
    resp = VoiceResponse()

    # # Read a message aloud to the caller
    # resp.say("This is El Mingle", voice='Polly.Salli', rate='100%')
    # resp.say("A service for Connecting the Elderly!)", voice='Polly.Salli', rate='100%')
    # resp.say("Ready to get chat chatty with that", voice='Polly.Emma', rate='100%')
    # resp.say("granny or grandpa", voice='Polly.Emma', rate='85%')
    # resp.say("of your dreams? Please say your name, age, gender identity, and what you are looking for.", voice='Polly.Emma', rate='100%')

    # Use <Record> to record the caller's message
    resp.record(timeout=1, action="/recording", method="POST")

    return str(resp)

@app.route("/recording", methods=['GET', 'POST'])
def recording_received():
    
    print(request.form["RecordingUrl"])
    recordingURL = request.form["RecordingUrl"]
    userNumber = request.values.get('From')

    # resp = VoiceResponse()
    # resp.say("Nice to meet you. In just a few moments you'll be speaking to the grandpapi or grandmommy of your dreams! Sit tight while we find you a match that will warm your heart!", voice='Polly.Emma')

    create_new_profile(userNumber, recordingURL)

    match_number = check_available(userNumber)

    if match_number == -1:
        print("no available users online, connecting to new conference call")
    else:
        print("matching you with a user")

    # Start with a <Dial> verb
    with Dial() as dial:
        # If the caller is our MODERATOR, then start the conference when they
        # join and end the conference when they leave
        if request.values.get('From') == MODERATOR:
            dial.conference(
                'My conference',
                start_conference_on_enter=True,
                end_conference_on_exit=True)
        else:
            # Otherwise have the caller join as a regular participant
            dial.conference('My conference', start_conference_on_enter=False)

    resp.append(dial)

    return str(resp)

def create_new_profile(phoneId, url):
    
    text = 'example chars'
    
    data = {
    u'status': u'waiting',
    u'intro_url': url,
    u'number':phoneId,
    u'characteristics':text, 
    }

    db.collection(u'user_profiles').document(phoneId).set(data)
    
def check_available(phoneId):
    similarity_dict = {}

    # retrieve caller characteristics
    caller = db.collection(u'user_profiles').document(phoneId)
    caller_chars = caller.get().to_dict()['characteristics']

    docs = db.collection(u'user_profiles').stream()
    for doc in docs:
        user = doc.to_dict()
        try:
            if phoneId == user["number"]:
                continue
            try:
                if user["status"] == 'waiting':
                    user_chars = user.get('characterstics')
                    similarity_dict[compute_similarity(caller_chars, user_chars)] = user["number"]
            except:
                print("none")
        except:
            print("can't find number")

    if len(similarity_dict) == 0:
        return -1

    best_similarity_score = max(similarity_dict.keys())

    match_number = similarity_dict[best_similarity_score]
    return match_number
    


def compute_similarity(caller_chars, user_chars):
    caller_charList = caller_chars.split(",")
    charList=user_chars.split(",")
    res = len(set(caller_char_list) & set(charList)) / float(len(set(caller_char_list) | set(charList))) * 100
    return res

if __name__ == "__main__":
    app.run(debug=True)