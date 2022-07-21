# Bulk WHOIS calls from a domain names list

Bulk WHOIS is a Python script to call WHOIS from a domain names list
(like [this sample](input.txt)). It reads a YAML configuration file,
calls WHOIS for every domain name in a list and writes a CSV file with
domain name and expiration date columns.

## Requirements

* Python 3.6+
* [python-whois](<https://pypi.org/project/python-whois/>)
* [ConfigObj](<https://github.com/DiffSK/configobj>)

> It is required to install ConfigObj from its GitHub repo, not from PyPI.
> Otherwise this script could not work.

## Installation

Not required. Clone this repository and use `bulkwhois.py` as described
below.

## Usage

Bulk WHOIS script utilizes configuration and spec files that might look like
these [configuration](bulkwhois.conf) and [spec](bulkwhoisspec.conf) samples.
If you rename `bulkwhois.py` then you need to rename configuration and spec
files accordingly. Keep these three files in the same directory.

The script does delays between WHOIS calls for avoiding to be blocked.
Every delay is calculated as a random value between `dmin` and `dmax`.

## TODO

* Add logging.
* Create a PyPI package.
