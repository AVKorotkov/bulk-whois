#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Bulk WHOIS calls from a domain names list."""

import random
import time
import argparse
import datetime
import csv
from pathlib import Path
import confuse
import whois


def random_sleep(delay_min, delay_max):
    """Sleep for random time in the given range."""
    # random delay in range (in seconds)
    delay = random.randint(delay_min, delay_max)/1000
    time.sleep(delay)


def get_config():
    """Get keys/values from YAML configuration file and/or options."""
    script_name = Path(__file__).stem
    conf_name = script_name + '.yaml'
    conf_path = Path(__file__).with_name(conf_name).absolute()
    conf = confuse.Configuration(script_name)
    conf.set_file(conf_path)
    desc = 'Get expiration dates for a list of domain names'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--input', type=str, help='input file for list of domain names')
    parser.add_argument('--output', type=str, help='output CSV file')
    parser.add_argument(
        '--dmin',
        type=int,
        help='min delay (in ms) between whois calls',
        dest='delay.min'
    )
    parser.add_argument(
        '--dmax',
        type=int,
        help='max delay (in ms) between whois calls',
        dest='delay.max'
    )
    args = parser.parse_args()
    conf.set_args(args, dots=True)
    return conf


def main():
    """Process all domain names from given list."""
    # get configuration keys/values
    config = get_config()
    input_file = config['input'].get()
    input_path = Path(input_file).absolute()
    output_file = config['output'].get()
    output_path = Path(output_file).absolute()
    delay_min = config['delay']['min'].get(int)
    delay_max = config['delay']['max'].get(int)
    # read input file, call WHOIS for every domain name and write the result
    with open(output_path, 'w', encoding='utf-8') as ofile:
        writer = csv.writer(ofile)
        writer.writerow(['domain name', 'expiration date'])
        with open(input_path, 'r', encoding='utf-8') as ifile:
            for line in ifile:
                domain = line.strip()
                if domain:
                    try:
                        req = whois.whois(domain)
                        exp = req.expiration_date
                        # expiration date could be a datetime or a list
                        if isinstance(exp, datetime.datetime):
                            exp = exp.strftime('%F %T')
                        elif isinstance(exp, list):
                            exp = exp[0].strftime('%F %T')
                        else:
                            exp = 'error'
                    except ConnectionError as err:
                        print(f'WHOIS error {err}')
                        exp = 'error'

                    writer.writerow([domain, exp])
                    random_sleep(delay_min, delay_max)


main()
