# DynDNS OVH

DynDNS update your dns entry for you.

## Requirements

- Pipenv

## Installation

> From source

``` bash
poetry install
```

## Usage

``` bash
poetry run python dydns MYHOSTNAME
````

The cli ask your username and password of your DynDNS OVH account. [En savoir plus](https://docs.ovh.com/fr/domains/utilisation-dynhost/#etape-1-creer-un-utilisateur-dynhost)

## Help

```bash
Usage: dyndns [OPTIONS] HOSTNAME

  Dyndns can update a DynDNS at OVH.

Options:
  --username TEXT                The name of your DynDNS user.
  --password TEXT                The password of your DynDNS user.
  --scheduling-duration INTEGER  The scheduling duration in seconds.
                                 Default time: 10s 
  --help                         Show this message and exit.
```

## Environment variables

| Variables        	| Definition                       	|
|-----------------	|----------------------------------	|
| DYNDNS_USERNAME 	| The name of the DynDNS user.     	|
| DYNDNS_PASSWORD 	| The passowrd of the DynDNS user. 	|
| DYNDNS_HOSTNAME 	| The hostname to update.          	|
