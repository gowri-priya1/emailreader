import requests
from imapclient import IMAPClient
import time
from email.header import decode_header

def extract_address(address_obj):
    if isinstance(address_obj, tuple):
        if hasattr(address_obj[0], 'decode'):
            name, email_address = decode_header(address_obj[0])[0]

            # Decode name and email_address if they are bytes
            if name and isinstance(name, bytes):
                name = name.decode('utf-8', errors='ignore')
            if email_address and isinstance(email_address, bytes):
                email_address = email_address.decode('utf-8', errors='ignore')

            return name, email_address
        else:
            return address_obj[0], None
    else:
        return str(address_obj), None

def send_whatsapp_message(api_key, phone_number, sender_name, sender_email, subject):
    api_url = 'https://graph.facebook.com/v17.0/131254153412771/messages'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:{phone_number}",
        "type": "template",
        "template": {
            "name": "your_template_name",  # Replace with your template name
            "language": {
                "code": "en"  # Replace with the appropriate language code
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": f"You have received a new email:"
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": f"Name: {sender_name}"
                        },
                        {
                            "type": "text",
                            "text": f"Sender Email ID: {sender_email}"
                        },
                        {
                            "type": "text",
                            "text": f"Subject: {subject}"
                        }
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"Message sent to {phone_number}")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

def read_emails_real_time(email_username, email_password, whatsapp_api_key, whatsapp_recipient_number):
    with IMAPClient('imap.gmail.com') as client:
        client.login(email_username, email_password)
        client.select_folder('inbox')

        processed_ids = set()

        print("Monitoring for new emails. Press Ctrl+C to exit.")

        try:
            while True:
                messages = client.search(['UNSEEN'])

                for uid, message_data in client.fetch(messages, ['ENVELOPE']).items():
                    envelope = message_data[b'ENVELOPE']
                    email_id = envelope.message_id

                    if email_id not in processed_ids:
                        # Use b'' to represent an empty bytes-like object
                        subject, encoding = decode_header(envelope.subject or b'')[0]

                        # Ensure that the subject is a string
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else 'utf-8', 'ignore')

                        subject_str = subject if subject else "No Subject"
                        name, from_email = extract_address(envelope.from_)

                        # Update the send_whatsapp_message function to include dynamic content
                        send_whatsapp_message(
                            whatsapp_api_key,
                            whatsapp_recipient_number,
                            sender_name=name,  # Use the sender's name or another identifier
                            sender_email=from_email,
                            subject=subject_str
                        )

                        # Print the content (optional)
                        print(f"you received mail from: {from_email} Subject: {subject_str}")

                        processed_ids.add(email_id)

                time.sleep(1)

        except KeyboardInterrupt:
            print("\nExiting program.")

if __name__ == "__main__":
    # Replace the following placeholders with your actual values
    email_username = 'shanmugasundaramanvi@gmail.com'
    email_password = 'bxjj gwue resw trhz'
    whatsapp_api_key = 'EAAWYZBS5pwhQBO4ONZCGWA4sscQvFHazZAxB0wwHcGXQR0yWIstoT1ZAyLDjNZBtlPBuDQYB2ScpoJzCHZCCO3ybMZBScDek8Bmcx4ANNraNoXZALi8nh51SuE6AXgZCyD6oGHgrZApKXwdMqpk5ZAG8LmSq0VGlWzCfGU0ux25b7vl2wYih1qVahDuZBag4gZBkrMqaSSbbX2910LCAa4wqBOf9lBrUrUG4ZD'
    whatsapp_recipient_number = '+919363127665'

    read_emails_real_time(email_username, email_password, whatsapp_api_key, whatsapp_recipient_number)

