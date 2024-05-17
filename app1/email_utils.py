import requests
# from email_utils import send_email

def send_email(api_key, subject, sender, recipient, body_html):
    api_url = 'https://api.elasticemail.com/v2/email/send'

    payload = {
        'apikey': api_key,
        'subject': subject,
        'from': sender,
        'to': recipient,
        'bodyHtml': body_html
    }

    response = requests.post(api_url, data=payload)

    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print(f'Failed to send email. Status code: {response.status_code}, Response: {response.text}')

# Replace these with your actual API key and email details
api_key = '75EDDFB48F9D8B13E8614AD4E3CE09EF41E780DC5BDF913D5672E8E84D2D916AD417AB2A4B6C59F11603D0A996EBAE09'
subject = 'Growmore'
sender = 'Info@socialforyoou.com'
recipient = 'web516399@gmail.com'
body_html = '<p>Hello, this is a test email.</p>'

# Call the function to send the email
send_email(api_key, subject, sender, recipient, body_html)
