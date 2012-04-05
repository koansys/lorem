#!/usr/bin/env python
# encoding: utf-8

import sys
import logging
from csv import DictReader      # need to do ones with no header line

from transform import email, first_name, first_last_name, host_name, ip, last_name, person_name, text, url, username


transforms = {
    'email': email,
    'first' : first_name,
    'first_last_name': first_last_name,
    'first_name' : first_name,
    'firstlast': first_last_name,
    'host' : host_name,
    'host_name' : host_name,
    'ip': ip,
    'last' : last_name,
    'last_name' : last_name,
    'person' : person_name,
    'person_name' : person_name,
    'text': text,
    'url': url,
    'url': url,
    'user': username,
    'username': username,
    }
logging.basicConfig(level=logging.INFO)

# Do CSV first, read from stdin before we worry about arg parsing
# use csv.Sniffer has_header

args = sys.argv[1:]
fields = dict([arg.split('=') for arg in args])

logging.info('fields=%s' % fields)

csv = DictReader(sys.stdin)
fieldnames = csv.fieldnames
for field, transform in fields.items():
    if field not in fieldnames:
        raise RuntimeError("Requested field name '%s' not in CSV fields: %s" % (field, fieldnames))
    if transform not in transforms:
        raise RuntimeError("Requested field name '%s' not in transform names: %s" % (field, transforms.keys()))

logging.info("csv fieldnames=%s" % fieldnames)
for row in csv:
    logging.info("row before: %s" % row)
    for field, transform in fields.items():
        #import pdb; pdb.set_trace()
        row[field] = transforms[transform](row[field])
    logging.info("row  after: %s" % row)





