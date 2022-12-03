from fritzconnection.lib.fritzstatus import FritzStatus
from datetime import datetime
from requests import get
import upnpclient

"""
Several variants of the same function are provided below.
Choose the one that suits your situation best and change the code in main.py accordingly.
getip_fritz() can be used if the router is a Fritz!Box. The function is fast and doesn't require third party services.
getip_ipify() can be used whatever router is used. The function is fast uses the third party service ipify.
getip_upnp() can be used whatever router is used. The funtion doesn't use third party services but is relatively slow.
All 3 function return a dictionary with 2 keys: datetime and public_ip.
"""


def getip_fritz():
    """
    Get the public IP-address of a Fritz!Box. No external services needed.
    :return: dict('datetime': str, 'public_ip': str)
    """
    public_ip = None
    try:
        public_ip = FritzStatus(address='192.168.178.1').external_ip
    finally:
        return {"datetime": str(datetime.now()), "public_ip": public_ip}


def getip_ipify():
    """
    Get the public IP-address by using the service ipify (https://www.ipify.org/)
    :return: dict('datetime': str, 'public_ip': str)
    """
    public_ip = None
    try:
        public_ip = get('https://api.ipify.org').content.decode('utf8')
    finally:
        return {"datetime": str(datetime.now()), "public_ip": public_ip}


def getip_upnp():
    """
    Get the public IP-address by using UPnP (should work with all routers)
    :return: dict('datetime': str, 'public_ip': str)
    """
    public_ip = None
    try:
        devices = upnpclient.discover()
        for device in devices:
            if 'WANIPConn1' in device.service_map:
                public_ip = device.WANIPConn1.GetExternalIPAddress()
                break
    finally:
        return {"datetime": str(datetime.now()), "public_ip": public_ip['NewExternalIPAddress']}
