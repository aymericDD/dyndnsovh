from dyndns import get_public_ip, update_dns_entry, NoChangeError, BadFQDNError
import time
import logging
import click
import os

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

SCHEDULING_DURATION_SECONDS_DEFAULT: str = 10


@click.command()
@click.argument("hostname")
@click.option(
    "--username",
    prompt=True,
    help="The username of your DynDNS: https://docs.ovh.com/fr/domains/utilisation-dynhost/#etape-1-creer-un-utilisateur-dynhost",
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    help="The password of your DynDNS: https://docs.ovh.com/fr/domains/utilisation-dynhost/#etape-1-creer-un-utilisateur-dynhost",
)
@click.option(
    "--scheduling-duration",
    required=False,
    default=SCHEDULING_DURATION_SECONDS_DEFAULT,
    help="The scheduling duration in seconds. Default time: {}s".format(
        SCHEDULING_DURATION_SECONDS_DEFAULT
    ),
)
def dyndns_cli(hostname: str, username: str, password: str, scheduling_duration: int):
    """Dyndns can update a DynDNS at OVH."""
    start_dyndns(hostname, username, password, scheduling_duration)


def start_dyndns(hostname: str, username: str, password: str, scheduling_duration: int):
    logging.info("Start DynDNS")
    logging.info("Scheduling duration: '%ss'", scheduling_duration)
    logging.info("Hostname to update: '%s'", hostname)
    logging.info("User: '%s'", username)

    CURRENT_IP = None
    TTL_DEFAULT: int = 144
    TTL_CACHE: int = TTL_DEFAULT

    while True:
        TTL_CACHE -= 1

        if TTL_CACHE < 0:
            CURRENT_IP = None
            TTL_CACHE = TTL_DEFAULT

        public_ip: str = get_public_ip()

        if public_ip != CURRENT_IP:
            logging.info("The '%s' public IP has changed.", public_ip)
            try:
                logging.info("Start to update '%s' hostname.", hostname)

                update_dns_entry(public_ip, hostname, username, password)
                logging.info("The '%s' hostname has been update.", hostname)
            except NoChangeError:
                logging.info("The '%s' hostname does not need to be updated.", hostname)
            except BadFQDNError:
                logging.error("The '%s' hostname does not exist.", hostname)
                os.abort()
            except ValueError:
                logging.error(
                    "Could not update the public IP for '%s' hostname with '%s' IP.",
                    hostname,
                    public_ip,
                )
                time.sleep(scheduling_duration)
                continue

            CURRENT_IP = public_ip
        else:
            logging.info("No need to change the IP for '%s' hostname.", hostname)

        time.sleep(scheduling_duration)


if __name__ == "__main__":
    dyndns_cli(auto_envvar_prefix="DYNDNS")
