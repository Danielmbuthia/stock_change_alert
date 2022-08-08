from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from dotenv import dotenv_values

config = dotenv_values()
TOKEN = config.get("TWILIO_TOKEN")
ACCOUNT = config.get("TWILIO_ACCOUNT")
SENDER_ID = config.get("TWILIO_SENDER_ID")


class Sms:
    def __init__(self, number, message):
        self.number = number
        self.message = message

    def send(self):
        client = Client(ACCOUNT, TOKEN)
        try:
            message = client.messages.create(to=self.number, from_=SENDER_ID,
                                             body=self.message)
            return message
        except TwilioRestException as e:
            return e
