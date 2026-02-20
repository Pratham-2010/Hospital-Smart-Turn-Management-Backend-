
from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
FROM_NUMBER = os.getenv("FROM_NUMBER")



client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_sms(to_number, message):

    print(f"[SMS] To {to_number}: {message}")
    client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=to_number
    )


def notify_if_near_turn(patients):

    for index, patient in enumerate(patients):

        if index <= 1 and patient["status"] == "waiting":

            message = (
                f"Hello {patient['name']}, "
                "your hospital turn is coming soon."
            )

            send_sms(patient["phone"], message)



