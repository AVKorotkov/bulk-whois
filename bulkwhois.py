#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Bulk WHOIS calls from a domain names list."""

import random
import time
import argparse
import datetime
from pathlib import Path
import confuse
import whois

def random_sleep():
    """Sleep for random time in the given range."""
    # random delay in range (in seconds)
    delay = random.randint(delay_min, delay_max)/1000
    time.sleep(delay)

def get_config():
    """Get keys/values from YAML configuration file and/or options."""
    script_name = Path(__file__).stem
    conf_name = script_name + '.yaml'
    conf_path = Path(__file__).with_name(conf_name).absolute()
    print(conf_path)
    conf = confuse.Configuration(script_name)
    conf.set_file(conf_path)
    desc = 'Get expiration dates for a list of domain names'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='input file for list of domain names')
    parser.add_argument('--output', type=str, help='output CSV file')
    parser.add_argument('--dmin', type=int, help='min delay (in ms) between whois calls', dest='delay.min')
    parser.add_argument('--dmax', type=int, help='max delay (in ms) between whois calls', dest='delay.max')
    args = parser.parse_args()
    conf.set_args(args, dots=True)
    return conf

def main():
    """Process all domain names from given list."""
    with open (output_path, 'w', encoding='utf-8') as ofile:
        ofile.write('domain name,expiration date\n')
        with open (input_path, 'r', encoding='utf-8') as ifile:
            for line in ifile:
                domain = line.strip()
                if domain:
                    print(domain)
                    try:
                        req = whois.whois(domain)
                        exp = req.expiration_date
                        print(isinstance(exp, datetime.datetime))
                        print(isinstance(exp, list))
                        if isinstance(exp, datetime.datetime):
                            exp = exp.strftime('%F %T')
                            print(exp)
                        elif isinstance(exp, list):
                            exp = exp[0].strftime('%F %T')
                            print(exp)
                        else:
                            exp = 'error'
                    except Exception as err:
                        print(f'WHOIS error {err}')
                        exp = 'error'
                        # pass

                    ofile.write(f'{domain},{exp}\n')
                    random_sleep()

# get_config()
# sys.exit()
config = get_config()
input_file = config['input'].get()
# input_path = Path(__file__).with_name(input_file).absolute()
input_path = Path(input_file).absolute()
output_file = config['output'].get()
# output_path = Path(__file__).with_name(output_file).absolute()
output_path = Path(output_file).absolute()
# logging = config['logging'].get(bool)
# interactive = config['interactive'].get(bool)
# verbose = config['verbose'].get(bool)
delay_min = config['delay']['min'].get(int)
delay_max = config['delay']['max'].get(int)
print(input_file)
print(input_path)
print(output_file)
print(output_path)
# print(logging)
# print(interactive)
# print(verbose)
print(delay_min)
print(delay_max)
# random_sleep()

# print(config.config_dir())
# main()
