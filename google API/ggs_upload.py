from google.cloud import storage
import urllib.request

source_file_name="http://api.twilio.com/2010-04-01/Accounts/ACea8ab3fe5e5886713b6248a77d2e6044/Recordings/REc608fdadf93db987c00d6e5b984f9596"
project_id = 'ElMingo'
bucket_name = 'bostonhack_elmingo'
destination_folder_path="wav_intro"

storage_client = storage.Client()


def gapiUploadUsingURL(url, pid, bn, fp):
	print("uploading file at: %s\n"%url)
	fName = url.split("/")[-1]
	fName = "{}.wav".format(fName)
	print("Save as file: %s\n"%fName)

	file = urllib.request.urlopen(url)

	bucket = storage_client.get_bucket(bn)
	blob = bucket.blob("{}/{}".format(fp, fName))

	blob.upload_from_string(file.read(), content_type='sound/wav')

	return fName







if __name__=='__main__':
	file_name = gapiUploadUsingURL(source_file_name, project_id, 
								bucket_name, destination_folder_path)
	print(file_name)