#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Bulk WHOIS calls from a domain names list."""

import argparse
import datetime
import csv
import sys
import time
from random import randint
from pathlib import Path
import whois
from configobj import ConfigObj, ConfigObjError, flatten_errors
from configobj.validate import Validator


def get_config() -> ConfigObj:
    """Parse configuration file.

    :raises ConfigObjError: Can't read config/spec file(s).
    :raises IOError: Can't read config/spec file(s).
    :return: configuration parameters
    :rtype: ConfigObj
    """
    try:
        conf = ConfigObj(CONF, configspec=SPEC, file_error=True)
    except (ConfigObjError, IOError) as err:
        print(err)
        sys.exit(1)

    return conf


def validate_config(conf: ConfigObj) -> None:
    """Validate configuration file.

    :param conf: Configuration parameters
    :type conf: ConfigObj
    """
    # print(type(conf))
    val = Validator()
    test = conf.validate(val, preserve_errors=True)
    if test is not True:
        print('Failed validation:')
        for (section_list, key, _) in flatten_errors(conf, test):
            section = ', '.join(section_list)
            if key is None:
                print(f'  The following section is missing: [{section}]')
            else:
                print(f'  The <{key}> key in the section [{section}]')
        sys.exit(2)


def check_min_and_max(delay_min: int, delay_max: int) -> None:
    """Check maximum and minimum delays.

    :param delay_min: Minimum delay, in milliseconds
    :type delay_min: int
    :param delay_max: Maximum delay, in milliseconds
    :type delay_max: int
    :raises ValueError: Exit if minimum delay is greater than maximum delay
    """
    try:
        if delay_min > delay_max:
            msg = (f'Minimum delay ({delay_min}) must not be greater '
                   f'than maximum delay ({delay_max}).'
                   )
            raise ValueError(msg)
    except ValueError as err:
        print(err)
        sys.exit('Check these values in your configuration file. Exiting now.')


def get_args() -> argparse.Namespace:
    """Parse command line arguments.

    :raises ArgumentError: wrong argument(s).
    :return: command line arguments
    :rtype: argparse.Namespace
    """
    desc = 'Get expiration dates for a list of domain names'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='input file for the given list of domain names'
    )
    parser.add_argument(
        '-o',
        '--outfile',
        type=str,
        help='output CSV file'
    )
    parser.add_argument(
        '--dmin',
        type=int,
        help='min delay (in ms) between whois calls',
        dest='delay_min'
    )
    parser.add_argument(
        '--dmax',
        type=int,
        help='max delay (in ms) between whois calls',
        dest='delay_max'
    )
    args = parser.parse_args()
    return args


def set_config() -> dict:
    """Set the final configuration by merging the given
    configuration file and command line arguments

    :return: Configuration options overwritten by command line arguments
    :rtype: dict
    """
    config = get_config()
    validate_config(config)
    check_min_and_max(config['delay']['min'], config['delay']['max'])
    # current configation options from the given configation file
    cnf = {}
    cnf['infile'] = config['data']['input']
    cnf['outfile'] = config['data']['output']
    cnf['delay_min'] = config['delay']['min']
    cnf['delay_max'] = config['delay']['max']
    args = get_args()
    # overwrite options from the given configation file
    # by command line arguments
    for arg in vars(args):
        if vars(args)[arg] is not None:
            cnf[arg] = vars(args)[arg]

    return cnf


def random_sleep(delay_min: int, delay_max: int) -> None:
    """Sleep for a random time (in seconds) in the given range.

    :param delay_min: Minimum delay, in milliseconds
    :type delay_min: int
    :param delay_max: Maximum delay, in milliseconds
    :type delay_max: int
    """
    # random delay in the given range (in seconds)
    delay = randint(delay_min, delay_max) / 1000
    time.sleep(delay)


def main():
    """Process all domain names from the given list."""
    # set the final options
    opts = set_config()
    input_path = Path(opts['infile']).absolute()
    output_path = Path(opts['outfile']).absolute()
    # read input file, call WHOIS for every domain name and write the result
    with open(output_path, 'w', encoding='utf-8') as ofile:
        writer = csv.writer(ofile)
        writer.writerow(['domain name', 'expiration date'])
        with open(input_path, 'r', encoding='utf-8') as ifile:
            for line in ifile:
                domain = line.strip()
                if domain:
                    try:
                        print(f'Get domain: {domain} expiration date...')
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
                        print(f'WHOIS error: {err}')
                        exp = 'error'

                    writer.writerow([domain, exp])
                    random_sleep(opts['delay_min'], opts['delay_max'])


if __name__ == '__main__':
    script_name = Path(__file__).stem
    conf_name = script_name + '.conf'
    spec_name = script_name + 'spec.conf'
    # Configuration file absolute path
    CONF = Path(__file__).with_name(conf_name).absolute()
    # Spec file absolute path
    SPEC = Path(__file__).with_name(spec_name).absolute()
    main()
