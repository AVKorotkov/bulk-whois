#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Bulk WHOIS calls from a domain names list."""

import sys
import random
import time
import argparse
import datetime
from pathlib import Path
import confuse
import whois
