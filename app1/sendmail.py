import requests
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings

def send_register_mail(email):
    subject = 'You have successfully completed your Registration'
    # url_link = f'http://127.0.0.1:8000/reset_password/{token}/'
    # print('25', url_link)
    # message = f'Hi, click on the link to reset your password: {url_link}'

    # Replace these with your actual AuthKey.io credentials and recipient data
    auth_key = '362abe918aa57dcf'  # Your AuthKey.io API key
    recipient_mobile = '8081337678'  # Recipient's mobile number
    recipient_email = email  # Recipient's email address
    country_code = '91'  # Country code (e.g., '91' for India)
    event_id = '315'  # Event ID
    recipient_name = 'shivani'  # Recipient's name
    company = 'GROWMORE INTERNATIONAL LIMITED'  # Your company name

    # Construct the URL with the URL link
    url = f"https://api.authkey.io/request?authkey={auth_key}&email={recipient_email}&country_code={country_code}&eid={event_id}&name={recipient_name}&company={company}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Use Django's send_mail to send the email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return JsonResponse({'message': 'URL link and email sent successfully'})
        else:
            return JsonResponse({'message': f'Failed to send email. AuthKey.io API error: {response.text}'}, status=500)
    except Exception as e:
        return JsonResponse({'message': f'Failed to send email. Exception: {str(e)}'}, status=500)

def send_forget_password_mail(email):
    subject = 'Your Password Has Been Successfully Reset'
    # url_link = f'http://127.0.0.1:8000/reset_password/{token}/'
    # print('25', url_link)
    # message = f'Hi, click on the link to reset your password: {url_link}'

    # Replace these with your actual AuthKey.io credentials and recipient data
    auth_key = '362abe918aa57dcf'  # Your AuthKey.io API key
    recipient_mobile = '8081337678'  # Recipient's mobile number
    recipient_email = email  # Recipient's email address
    country_code = '91'  # Country code (e.g., '91' for India)
    event_id = '317'  # Event ID
    recipient_name = 'shivani'  # Recipient's name
    company = 'GROWMORE INTERNATIONAL LIMITED'  # Your company name

    # Construct the URL with the URL link
    url = f"https://api.authkey.io/request?authkey={auth_key}&email={recipient_email}&country_code={country_code}&eid={event_id}&name={recipient_name}&company={company}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Use Django's send_mail to send the email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return JsonResponse({'message': 'URL link and email sent successfully'})
        else:
            return JsonResponse({'message': f'Failed to send email. AuthKey.io API error: {response.text}'}, status=500)
    except Exception as e:
        return JsonResponse({'message': f'Failed to send email. Exception: {str(e)}'}, status=500)

def send_change_password_mail(email):
    subject = 'Your Password Has Been Successfully Change'
    # url_link = f'http://127.0.0.1:8000/reset_password/{token}/'
    # print('25', url_link)
    # message = f'Hi, click on the link to reset your password: {url_link}'

    # Replace these with your actual AuthKey.io credentials and recipient data
    auth_key = '362abe918aa57dcf'  # Your AuthKey.io API key
    recipient_mobile = '8081337678'  # Recipient's mobile number
    recipient_email = email  # Recipient's email address
    country_code = '91'  # Country code (e.g., '91' for India)
    event_id = '312'  # Event ID
    recipient_name = 'shivani'  # Recipient's name
    company = 'GROWMORE INTERNATIONAL LIMITED'  # Your company name

    # Construct the URL with the URL link
    url = f"https://api.authkey.io/request?authkey={auth_key}&email={recipient_email}&country_code={country_code}&eid={event_id}&name={recipient_name}&company={company}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Use Django's send_mail to send the email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return JsonResponse({'message': 'URL link and email sent successfully'})
        else:
            return JsonResponse({'message': f'Failed to send email. AuthKey.io API error: {response.text}'}, status=500)
    except Exception as e:
        return JsonResponse({'message': f'Failed to send email. Exception: {str(e)}'}, status=500)


def send_place_order_mail(email):
    subject = 'Your Order Has Been Successfully Placed! Thank You for Shopping with Us!'
    # url_link = f'http://127.0.0.1:8000/reset_password/{token}/'
    # print('25', url_link)
    # message = f'Hi, click on the link to reset your password: {url_link}'

    # Replace these with your actual AuthKey.io credentials and recipient data
    auth_key = '362abe918aa57dcf'  # Your AuthKey.io API key
    recipient_mobile = '8081337678'  # Recipient's mobile number
    recipient_email = email  # Recipient's email address
    country_code = '91'  # Country code (e.g., '91' for India)
    event_id = '316'  # Event ID
    recipient_name = 'shivani'  # Recipient's name
    company = 'GROWMORE INTERNATIONAL LIMITED'  # Your company name

    # Construct the URL with the URL link
    url = f"https://api.authkey.io/request?authkey={auth_key}&email={recipient_email}&country_code={country_code}&eid={event_id}&name={recipient_name}&company={company}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Use Django's send_mail to send the email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return JsonResponse({'message': 'URL link and email sent successfully'})
        else:
            return JsonResponse({'message': f'Failed to send email. AuthKey.io API error: {response.text}'}, status=500)
    except Exception as e:
        return JsonResponse({'message': f'Failed to send email. Exception: {str(e)}'}, status=500)
