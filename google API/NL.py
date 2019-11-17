# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'Aside from course work, my passion for traveling was what prompted me to take part in the study aboard program in Dresden, Germany, in the spring of 2018 and Tokyo, Japan in the summer of 2017. While taking classes offered at both TU Dresden and Tokyo tech, I spent most of my off time traveling Europe and around the city. Combine with my study in the States, I believe that it is these experiences that taught me how to quickly adapt to changes in the environment and apply my ability in a different context. My passion for electronics and computers is also what prompts me to join the High-Performance Computing (HPC) club and continue to be an active member of the university maker space. My decision to take part in the leadership role of the BUHPC contained more than my interest in the subject matter; I wish to inspire others learning about HPC by sharing a subject that I enjoy learning. Similarly, by taking part in the engineering '
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

encoding_type = enums.EncodingType.UTF8

response = client.analyze_entities(document, encoding_type=encoding_type)
# Loop through entitites returned from the API
print(response.entities)



# for entity in response.entities:
# 	print(u"Representative name for the entity: {}".format(entity.name))
# 	# Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
# 	print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
# 	# Get the salience score associated with the entity in the [0, 1.0] range
# 	print(u"Salience score: {}".format(entity.salience))
# 	# Loop over the metadata associated with entity. For many known entities,
# 	# the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
# 	# Some entity types may have additional metadata, e.g. ADDRESS entities
# 	# may have metadata for the address street_name, postal_code, et al.
# 	for metadata_name, metadata_value in entity.metadata.items():
# 		print(u"\t{}: {}".format(metadata_name, metadata_value))

# 	# Loop over the mentions of this entity in the input document.
# 	# The API currently supports proper noun mentions.
# 	for mention in entity.mentions:
# 		print(u"\t\tMention text: {}".format(mention.text.content))
# 		# Get the mention type, e.g. PROPER for proper noun
# 		print(
# 		    u"\t\tMention type: {}".format(enums.EntityMention.Type(mention.type).name)
# 		)

# # Get the language of the text, which will be the same as
# # the language specified in the request or, if not specified,
# # the automatically-detected language.
# print(u"Language of the text: {}".format(response.language))
