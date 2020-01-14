import requests
import pytest
from dyndns.dyndns import get_public_ip, update_dns_entry, NoChangeError, BadFQDNError

from dyndns import __version__

TESTED_MODULE: str = "dyndns.dyndns."


def test_get_ip_public(mocker):
    # arrange
    expected_public_ip: str = "192.168.1.98"
    mock_requests = mocker.patch(TESTED_MODULE + "requests")
    mock_response = mocker.MagicMock()
    mock_response.text = expected_public_ip
    mock_requests.get.return_value = mock_response

    # action
    public_ip: str = get_public_ip()

    # assert
    assert expected_public_ip == public_ip


def test_request_to_update_dns_entry_success(mocker):
    # arrange
    expected_ip: str = "192.168.1.2"
    expected_hostname: str = "hostname"
    expected_username: str = "username"
    expected_password: str = "password"
    expected_url: str = "http://www.ovh.com/nic/update?system=dyndns&hostname={}&myip={}".format(
        expected_hostname, expected_ip
    )
    mock_requests = mocker.patch(TESTED_MODULE + "requests")
    mock_response = mocker.MagicMock()
    mock_response.text = "good {}".format(expected_ip)
    mock_requests.get.return_value = mock_response
    # action
    update_dns_entry(
        expected_ip, expected_hostname, expected_username, expected_password
    )

    # assert
    mock_requests.get.assert_called_once_with(
        expected_url, auth=(expected_username, expected_password)
    )


def test_request_to_update_dns_entry_error(mocker):
    # arrange
    mock_requests = mocker.patch(TESTED_MODULE + "requests")
    mock_response = mocker.MagicMock()
    mock_response.text = "fdqf {}".format("10.10.10.10")
    mock_requests.get.return_value = mock_response
    # action
    with pytest.raises(ValueError):
        update_dns_entry("10.10.10.10", "hostname", "username", "password")


def test_request_to_update_dns_entry_no_change(mocker):
    # arrange
    mock_requests = mocker.patch(TESTED_MODULE + "requests")
    mock_response = mocker.MagicMock()
    mock_response.text = "nochg {}".format("10.10.10.10")
    mock_requests.get.return_value = mock_response
    # action
    with pytest.raises(NoChangeError):
        update_dns_entry("10.10.10.10", "hostname", "username", "password")


def test_request_to_update_dns_entry_bad_fqdn(mocker):
    # arrange
    mock_requests = mocker.patch(TESTED_MODULE + "requests")
    mock_response = mocker.MagicMock()
    mock_response.text = "badfqdn"
    mock_requests.get.return_value = mock_response
    # action
    with pytest.raises(BadFQDNError):
        update_dns_entry("10.10.10.10", "hostname", "username", "password")
