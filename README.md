# Bulk WHOIS calls from a domain names list

Bulk WHOIS is a Python script to call WHOIS from a domain names list
(like [this sample](input.txt)). It reads a configuration file, calls
WHOIS for every domain name in a list and writes
a [CSV file](output.csv) with domain name and expiration date columns.

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

Key/values in a configuration file could be overwritten by command line
arguments:

```text
usage: bulkwhois.py [-h] [-i INFILE] [-o OUTFILE] [--dmin DELAY_MIN] [--dmax DELAY_MAX]

Get expiration dates for a list of domain names

options:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        input file for the given list of domain names
  -o OUTFILE, --outfile OUTFILE
                        output CSV file
  --dmin DELAY_MIN      min delay (in ms) between whois calls
  --dmax DELAY_MAX      max delay (in ms) between whois calls

```

The script does delays between WHOIS calls for avoiding to be blocked.
Every delay is calculated as a random value between `dmin` and `dmax`.

## TODO

* Add logging.
* Create a PyPI package.
