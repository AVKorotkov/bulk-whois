# Bulk WHOIS calls from a domain names list

Bulk WHOIS is a Python script to call WHOIS from a domain names list. It 
reads a YAML configuration file, calls WHOIS for every domain name in a 
list and writes a CSV file with domain name and expiration date columns.

## Requirements

* Python 3.x
* [python-whois](https://pypi.org/project/python-whois/)
* [Confuse](https://pypi.org/project/confuse/)

## Installation

Not required. Clone this repository and use `bulkwhois.py` as described 
below.

## Usage

Bulk WHOIS script utilizes configuration file that might look like [this 
sample](bulkwhois.yaml). If you rename `bulkwhois.py` then you need to 
rename a configuration file with the same name, but with the `yaml` 
extension. Keep both files in the same directory. 

Key/values in a configuration file could be overridden by command line 
options:

```text
usage: bulkwhois.py [-h] [--input INPUT] [--output OUTPUT] [--dmin DELAY.MIN] [--dmax DELAY.MAX]

Get expiration dates for a list of domain names

options:
  -h, --help        show this help message and exit
  --input INPUT     input file for list of domain names
  --output OUTPUT   output CSV file
  --dmin DELAY.MIN  min delay (in ms) between whois calls
  --dmax DELAY.MAX  max delay (in ms) between whois calls
```

The script does delays between WHOIS calls for avoiding to be blocked. 
Every delay is calculated as a random values between `dmin` and `dmax`.

## TODO

Add logging.
