from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Record

app = Flask(__name__)

recordingURL = ""

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("This is El Mingle", voice='Polly.Salli', rate='100%')
    resp.say("A service for Connecting the Elderly!)", voice='Polly.Salli', rate='100%')
    resp.say("Ready to get chatty with that", voice='Polly.Emma', rate='100%')
    resp.say("granny or grandpa", voice='Polly.Emma', rate='85%')
    resp.say("of your dreams? Please say your name, age, and what you are looking for.", voice='Polly.Emma', rate='100%')

    # Use <Record> to record the caller's message
    resp.record(timeout=1, action="/recording", method="POST")
    

    return str(resp)

@app.route("/recording", methods=['GET', 'POST'])
def recording_received():
    
    print(request.form["RecordingUrl"])
    recordingURL = request.form["RecordingUrl"]
    resp = VoiceResponse()
    resp.say("Nice to meet you. In just a few moments you'll be speaking to the granpapi ro granmommy of your dreams!", voice='Polly.Emma')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
