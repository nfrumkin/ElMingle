# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()
ENTITY_TYPE_TO_IGNORE = [8, 9, 10, 11, 12]

# The text to analyze
text = "Aside from course work, my passion for traveling was what prompted me to take part in the study aboard program in Dresden, Germany, in the spring of 2018 and Tokyo, Japan in the summer of 2017. While taking classes offered at both TU Dresden and Tokyo tech, I spent most of my off time traveling Europe and around the city. Combine with my study in the States, I believe that it is these experiences that taught me how to quickly adapt to changes in the environment and apply my ability in a different context. My passion for electronics and computers is also what prompts me to join the High-Performance Computing (HPC) club and continue to be an active member of the university maker space. My decision to take part in the leadership role of the BUHPC contained more than my interest in the subject matter; I wish to inspire others learning about HPC by sharing a subject that I enjoy learning. Similarly, by taking part in the engineering "

def gapiAnalysisText(text):
	document = types.Document(
	    content=text,
	    type=enums.Document.Type.PLAIN_TEXT)

	encoding_type = enums.EncodingType.UTF8

	response = client.analyze_entities(document, encoding_type=encoding_type)
	# Loop through entitites returned from the API


	key_words=list()

	for entity in response.entities:
		if (entity.type not in ENTITY_TYPE_TO_IGNORE):
			key_words.append(entity.name)

	key_words=list(dict.fromkeys(key_words))
	key_words.sort()
	return ",".join(map(str,key_words))


char_str= gapiAnalysisText(text)
print(char_str)
