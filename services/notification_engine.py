
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

        if index <= 2 and patient["status"] == "waiting":

            if index == 0:
                message = (
                    f"Hello {patient['name']}, "
                    "you are next in the queue. Please be ready."
                )
            elif index == 1:
                message = (
                    f"Hello {patient['name']}, "
                    "your turn is 1 number away."
                )
            else:
                message = (
                    f"Hello {patient['name']}, "
                    f"your turn is {index} numbers away."
                )

            send_sms(patient["phone"], message)



