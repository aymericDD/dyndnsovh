"""
DynDNS module.
Update your dns entry
"""
import requests


class NoChangeError(Exception):
    """
    Raised when the Ip is same as previous.
    """

    pass


class BadFQDNError(Exception):
    """
    Raised when the hostname to update does not exist.
    """

    pass


SUCCESS_UPDATE = "good"
SUCCESS_NO_CHANGE = "nochg"
ERROR_BADFQDN = "badfqdn"


def get_public_ip():
    """
    Get the public ip from ipv4.nsupdate.info web site.

    Return:
        The public IP.
    """
    response = requests.get("http://ipv4.nsupdate.info/myip")
    response.raise_for_status()

    return response.text


def update_dns_entry(new_ip: str, hostname: str, username: str, password: str):
    """
    Update the dns entry at OVH.

    Args:
        new_ip: The new IP public.
        hostname: The hostnam to update.
        username: The name of the DynDNS user.
        password: The password of the DynDNS user.

    Return:
        None

    Raises:
        NoChangeError: Raised when the Ip is same as previous.
        BadFQDNError: Raised when the hostname to update does not exist.
    """
    url = "http://www.ovh.com/nic/update?system=dyndns&hostname={}&myip={}".format(
        hostname, new_ip
    )
    response = requests.get(url, auth=(username, password),)
    response.raise_for_status()

    if SUCCESS_NO_CHANGE in response.text:
        raise NoChangeError()

    if ERROR_BADFQDN in response.text:
        raise BadFQDNError()

    if SUCCESS_UPDATE not in response.text:
        raise ValueError()
