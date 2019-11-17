from __future__ import division
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Record, Dial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from google.cloud import speech
from google.cloud.speech import enums as speech_enums
# from google.cloud.speech import types as speech_types
from google.cloud import storage
import urllib.request

import re
import sys
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums as lang_enums
from google.cloud.language import types as lang_types

# Instantiates a client
nlp_client = language.LanguageServiceClient()
ENTITY_TYPE_TO_IGNORE = [8, 9, 10, 11, 12]

# storage creditials
source_file_name="https://api.twilio.com/2010-04-01/Accounts/ACea8ab3fe5e5886713b6248a77d2e6044/Recordings/REc608fdadf93db987c00d6e5b984f9596"
project_id = 'ElMingo'
bucket_name = 'bostonhack_elmingo'
destination_folder_path="wav_intro"

app = Flask(__name__)

recordingURL = ""
MODERATOR = '+12034875958'

# Use a service account
cred = credentials.Certificate('/home/natasha/athena/Desktop/ElMingle/ElMingleCreds.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
stt_client = speech.SpeechClient()
storage_client = storage.Client()

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

    resp = VoiceResponse()
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

def gapiUploadUsingURL(url, pid, bn, fp):
	url_splitted = url.split("/")
	if(url_splitted[0]=='https:'):
		url_splitted[0]='http:'

	url="/".join(map(str,url_splitted))
	print("uploading file at: %s\n"%url)

	fName = url_splitted[-1]
	fName = "{}.wav".format(fName)
	print("Save as file: %s\n"%fName)

	file = urllib.request.urlopen(url)

	bucket = storage_client.get_bucket(bn)
	blob = bucket.blob("{}/{}".format(fp, fName))

	blob.upload_from_string(file.read(), content_type='sound/wav')

	return fName

def getSpeechTranscript(uri):
	audio = types.RecognitionAudio(uri=uri)


	config = types.RecognitionConfig(
	    encoding=speech_enums.RecognitionConfig.AudioEncoding.LINEAR16,
	    sample_rate_hertz=8000,
	    language_code='en-US')

	# Detects speech in the audio file
	response = client.recognize(config, audio)

	print(response.results)
	return response.results[0].alternatives[0].transcript

def gapiAnalysisText(text):
	document = types.Document(
	    content=text,
	    type=lang_enums.Document.Type.PLAIN_TEXT)

	encoding_type = lang_enums.EncodingType.UTF8

	response = client.analyze_entities(document, encoding_type=encoding_type)
	# Loop through entitites returned from the API


	key_words=list()

	for entity in response.entities:
		if (entity.type not in ENTITY_TYPE_TO_IGNORE):
			key_words.append(entity.name)

	key_words=list(dict.fromkeys(key_words))
	key_words.sort()
	return ",".join(map(str,key_words))

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def create_new_profile(phoneId, url):
    
    file_name = gapiUploadUsingURL(source_file_name, project_id, 
								bucket_name, destination_folder_path)

    speech_to_text = getSpeechTranscript(file_name)

    user_characteristics = gapiAnalysisText(speech_to_text)
    
    data = {
    u'status': u'waiting',
    u'intro_url': url,
    u'number':phoneId,
    u'characteristics':user_characteristics, 
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
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'zh-TW'  # a BCP-47 language tag
    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=speech_enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)

    streaming_config = speech.types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    
    app.run(debug=True)