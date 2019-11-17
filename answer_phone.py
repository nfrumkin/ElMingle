from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Record, Dial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

app = Flask(__name__)

recordingURL = ""
MODERATOR = '+19392190769'

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("This is El Mingle", voice='Polly.Salli', rate='100%')
    resp.say("A service for Connecting the Elderly!)", voice='Polly.Salli', rate='100%')
    resp.say("Ready to get chat chatty with that", voice='Polly.Emma', rate='100%')
    resp.say("granny or grandpa", voice='Polly.Emma', rate='85%')
    resp.say("of your dreams? Please say your name, age, gender identity, and what you are looking for.", voice='Polly.Emma', rate='100%')

    # Use <Record> to record the caller's message
    resp.record(timeout=1, action="/recording", method="POST")

    return str(resp)

@app.route("/recording", methods=['GET', 'POST'])
def recording_received():
    
    print(request.form["RecordingUrl"])
    recordingURL = request.form["RecordingUrl"]
    resp = VoiceResponse()
    resp.say("Nice to meet you. In just a few moments you'll be speaking to the grandpapi or grandmommy of your dreams! Sit tight while we find you a match that will warm your heart!", voice='Polly.Emma')

    # Start with a <Dial> verb
    with Dial() as dial:
        # If the caller is our MODERATOR, then start the conference when they
        # join and end the conference when they leave
        if request.values.get('From') == MODERATOR:
            dial.conference(
                'My conference',
                start_conference_on_enter=True,
                end_conference_on_exit=True, wait_url="https://carmine-eagle-9377.twil.io/assets/Robbie%20Williams%20-%20Beyond%20the%20Sea-%5BAudioTrimmer.com%5D.mp3")
        else:
            # Otherwise have the caller join as a regular participant
            dial.conference('My conference', start_conference_on_enter=False, wait_url="https://carmine-eagle-9377.twil.io/assets/Robbie%20Williams%20-%20Beyond%20the%20Sea-%5BAudioTrimmer.com%5D.mp3")

    resp.append(dial)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
