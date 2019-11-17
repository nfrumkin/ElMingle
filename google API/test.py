from google.cloud import texttospeech
from google.cloud.texttospeech import enums


def main():
	# list_voices()
	# Instantiates a client
	client = texttospeech.TextToSpeechClient()

	# Set the text input to be synthesized
	synthesis_input = texttospeech.types.SynthesisInput(text="Hello, please state your name and introduce little bit about yourself")

	# Build the voice request, select the language code ("en-US") and the ssml
	# voice gender ("neutral")
	voice = texttospeech.types.VoiceSelectionParams(
		name='en-US-Wavenet-E',
	    language_code='en-US',
	    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

	# Select the type of audio file you want returned
	audio_config = texttospeech.types.AudioConfig(
	    audio_encoding=texttospeech.enums.AudioEncoding.MP3, 
	    effects_profile_id=["telephony-class-application"])


	# Perform the text-to-speech request on the text input with the selected
	# voice parameters and audio file type
	response = client.synthesize_speech(synthesis_input, voice, audio_config)

	# The response's audio_content is binary.
	with open('output.mp3', 'wb') as out:
	    # Write the response to the output file.
	    out.write(response.audio_content)
	    print('Audio content written to file "output.mp3"')



def list_voices():

	client = texttospeech.TextToSpeechClient()

	# Performs the list voices request
	voices = client.list_voices()

	for voice in voices.voices:
		# Display the voice's name. Example: tpc-vocoded
		print('Name: {}'.format(voice.name))

		# Display the supported language codes for this voice. Example: "en-US"
		for language_code in voice.language_codes:
			print('Supported language: {}'.format(language_code))

		ssml_gender = enums.SsmlVoiceGender(voice.ssml_gender)

		# Display the SSML Voice Gender
		print('SSML Voice Gender: {}'.format(ssml_gender.name))

		# Display the natural sample rate hertz for this voice. Example: 24000
		print('Natural Sample Rate Hertz: {}\n'.format(
		voice.natural_sample_rate_hertz))


if __name__=='__main__':
	main()