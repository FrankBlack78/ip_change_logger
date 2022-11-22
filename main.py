#!/usr/bin/env python3
from fritzconnection.lib.fritzstatus import FritzStatus
from datetime import datetime
import json
import os
from functions import send_email

"""
Sending of emails can be activated or deactivated.
If activated a verified email-address with SendGrid and one or more recepients should be defined.
"""
SEND_MAIL = 'no'
VERIFIED_SENDER = 'verifiedsender@test.com'
MAIL_RECIPIENTS = [
    'recipient@test.com'
]


def main() -> 0:
    """
    Main-Loop
    :return: 0
    """
    # Define filepath where to store information about the public ip-address
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.json')

    # Try to open the file and read past data. If file does not exist, create dictionary with keys but no values.
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            past_data = json.load(f)
    except FileNotFoundError:
        past_data = {"datetime": "", "public_ip": ""}

    # Get current public ip-address of the FRITZ!Box
    public_ip = FritzStatus(address='192.168.178.1').external_ip

    # Create current data
    current_data = {"datetime": str(datetime.now()), "public_ip": public_ip}

    # Compare past data with current data
    if past_data['public_ip'] == current_data['public_ip']:
        current_timestamp = datetime.strptime(current_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        past_timestamp = datetime.strptime(past_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        diff_time = current_timestamp - past_timestamp
        print(f'Same IP-address since {str(diff_time)} (HH:MM:SS).')
        if SEND_MAIL == 'yes':
            for recipient in MAIL_RECIPIENTS:
                send_email(VERIFIED_SENDER,
                           recipient,
                           'Same public IP-address',
                           f'Same IP-address since {str(diff_time)} (HH:MM:SS).')
    else:
        # Calculate time-difference between old and new datetime
        current_timestamp = datetime.strptime(current_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        past_timestamp = datetime.strptime(past_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        diff_time = current_timestamp - past_timestamp
        print(f'Old IP-address was valid for {str(diff_time)} (HH:MM:SS).')
        # Save current-data as JSON-data to filepath
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)
        print(f'NEW PUBLIC IP: {public_ip}')
        if SEND_MAIL == 'yes':
            for recipient in MAIL_RECIPIENTS:
                send_email(VERIFIED_SENDER,
                           recipient,
                           'New public IP-address',
                           f'Old IP-address was valid for {str(diff_time)} (HH:MM:SS).\n'
                           f'New public IP-address: {public_ip}')
    return 0


if __name__ == '__main__':
    main()
