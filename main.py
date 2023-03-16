#!/usr/bin/env python3
from datetime import datetime
import json
import os
from f_signal import send_email
import f_getip
import configparser

# Global variables (Defined in config.ini)
config = configparser.ConfigParser()
config.read('config.ini')

GETIP = config['f_getip']['GETIP']
SEND_MAIL = config['f_signal'].getboolean('SEND_MAIL')
VERIFIED_SENDER = config['f_signal']['VERIFIED_SENDER']
MAIL_RECIPIENTS = config['f_signal']['MAIL_RECIPIENTS'].split()


def main() -> 0:
    """
    Main-Loop
    :return: 0
    """
    # Define filepath where to store information about the public ip-address
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.json')

    # Try to open the file and read past data. If file does not exist, create empty data list.
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            past_data = json.load(f)
    except FileNotFoundError:
        past_data = []

    # Find the latest record in past data
    latest_past_data_record = {}
    if len(past_data) > 0:
        dt_list = []
        for ds in past_data:
            dt_list.append(datetime.strptime(ds['datetime'], '%Y-%m-%d %H:%M:%S.%f'))
        for idx, ds in enumerate(past_data):
            if max(dt_list) == datetime.strptime(ds['datetime'], '%Y-%m-%d %H:%M:%S.%f'):
                latest_past_data_record = past_data[idx]

    # Get current data
    if GETIP == 'getip_fritz':
        current_data = [f_getip.getip_fritz()]
    elif GETIP == 'getip_ipify':
        current_data = [f_getip.getip_ipify()]
    elif GETIP == 'getip_upnp':
        current_data = [f_getip.getip_upnp()]
    else:
        return 1
    current_data_record = current_data[0]

    # Write current data to file
    data = past_data + current_data
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Compare past data with current data, determine outcome and signal
    # No past data available
    if len(latest_past_data_record) == 0:
        print(f'No past data. New public IP-address ({current_data_record["public_ip"]}).')
        if SEND_MAIL:
            for recipient in MAIL_RECIPIENTS:
                send_email(VERIFIED_SENDER,
                           recipient,
                           'New public IP-address',
                           f'No past data. New public IP-address ({current_data_record["public_ip"]}).')
    # Past data available
    else:
        # Sort past data in descending order
        past_data.sort(key=lambda x: datetime.strptime(x['datetime'], '%Y-%m-%d %H:%M:%S.%f'), reverse=True)

        # Determine oldest past data with identical public IP
        oldest_past_data_record = dict()
        for idx, ds in enumerate(past_data):
            if ds['public_ip'] == latest_past_data_record['public_ip']:
                oldest_past_data_record = ds
            else:
                break

        # Get timestamps of the datasets
        oldest_past_timestamp = datetime.strptime(oldest_past_data_record['datetime'].split('.')[0],
                                                  '%Y-%m-%d %H:%M:%S')
        latest_past_timestamp = datetime.strptime(latest_past_data_record['datetime'].split('.')[0],
                                                  '%Y-%m-%d %H:%M:%S')
        current_timestamp = datetime.strptime(current_data_record['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')

        # Changed public IP
        if latest_past_data_record['public_ip'] != current_data_record['public_ip']:
            # Calculate time difference
            diff_time = latest_past_timestamp - oldest_past_timestamp

            # Signal
            print(f'Old IP-address ({latest_past_data_record["public_ip"]}) was valid for {str(diff_time)} (HH:MM:SS).')
            print(f'New public IP-address: {current_data_record["public_ip"]}')
            if SEND_MAIL:
                for recipient in MAIL_RECIPIENTS:
                    send_email(VERIFIED_SENDER,
                               recipient,
                               'New public IP-address',
                               f'Old IP-address ({latest_past_data_record["public_ip"]}) was valid for {str(diff_time)} (HH:MM:SS).\n'
                               f'New public IP-address: {current_data_record["public_ip"]}')

        # Same public IP
        elif latest_past_data_record['public_ip'] == current_data_record['public_ip']:
            # Calculate time difference
            diff_time = current_timestamp - oldest_past_timestamp

            # Signal
            print(f'Same public IP-address ({current_data_record["public_ip"]}) since {str(diff_time)} (HH:MM:SS).')
            if SEND_MAIL:
                for recipient in MAIL_RECIPIENTS:
                    send_email(VERIFIED_SENDER,
                               recipient,
                               'Same public IP-address',
                               f'Same public IP-address ({current_data_record["public_ip"]}) since {str(diff_time)} (HH:MM:SS).')

        # Should not happen!
        else:
            return 1

    return 0


if __name__ == '__main__':
    main()
