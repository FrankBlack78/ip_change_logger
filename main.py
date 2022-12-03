#!/usr/bin/env python3
from datetime import datetime
import json
import os
from f_signal import send_email
import f_getip

"""
Which function of getting the public ip-address should be used?
Allowed are: getip_fritz, getip_ipify, getip_upnp
"""
GETIP = 'getip_fritz'

"""
Sending of emails can be activated or deactivated.
If activated a verified sender email-address with SendGrid and one or more recepients have to be defined.
"""
SEND_MAIL = False
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

    # Create current data
    if GETIP == 'getip_fritz':
        current_data = f_getip.getip_fritz()
    elif GETIP == 'getip_ipify':
        current_data = f_getip.getip_ipify()
    elif GETIP == 'getip_upnp':
        current_data = f_getip.getip_upnp()
    else:
        return 1

    # Compare past data with current data
    if past_data['public_ip'] == current_data['public_ip']:
        current_timestamp = datetime.strptime(current_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        past_timestamp = datetime.strptime(past_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        diff_time = current_timestamp - past_timestamp
        print(f'Same public IP-address ({current_data["public_ip"]}) since {str(diff_time)} (HH:MM:SS).')
        if SEND_MAIL:
            for recipient in MAIL_RECIPIENTS:
                send_email(VERIFIED_SENDER,
                           recipient,
                           'Same public IP-address',
                           f'Same public IP-address ({current_data["public_ip"]}) since {str(diff_time)} (HH:MM:SS).')
    else:
        # Calculate time-difference between old and new datetime
        current_timestamp = datetime.strptime(current_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        past_timestamp = datetime.strptime(past_data['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        diff_time = current_timestamp - past_timestamp
        print(f'Old IP-address ({past_data["public_ip"]}) was valid for {str(diff_time)} (HH:MM:SS).')
        # Save current-data as JSON-data to filepath
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)
        print(f'New public IP-address: {current_data["public_ip"]}')
        if SEND_MAIL:
            for recipient in MAIL_RECIPIENTS:
                send_email(VERIFIED_SENDER,
                           recipient,
                           'New public IP-address',
                           f'Old IP-address ({past_data["public_ip"]}) was valid for {str(diff_time)} (HH:MM:SS).\n'
                           f'New public IP-address: {current_data["public_ip"]}')
    return 0


if __name__ == '__main__':
    main()
