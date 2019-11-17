# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACc07d36f2bedb365988af5c81d578bfef'
auth_token = 'd7698b135d26730bf84600c176d6815f'
client = Client(account_sid, auth_token)

call = client.calls.create(
			record=True,
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+19392190769',
                        from_='+12512835337'
                    )

print(call.sid)