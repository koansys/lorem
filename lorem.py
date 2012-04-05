#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# SQLAlchemy seems like serious overkill for this app.
# Use simpler DBAPI2?
# - sqlite3 db built in
# - psycopg2 not
# - mysql-python

# CSV outputs to stdout
# DB done *in place*

# If we're going to use 3rd party DB library,
# might as well use 3rd party LoremIpsum generator?

# I expect this program would be invoked something like the following.
# CSV with header line:
#   ./lorem.py fodder.csv name=person url=url ip=ip host=host text=text
#   ./lorem.py - name=person url=url ip=ip host=host text=text < fodder.csv
# CSV without header line, access fields by their number, starting at 0
#   ./lorem.py 1=person 2=url 4=ip 6=host 2=text < fodder.csv
# SQL DB: Specify DB URL and list of table.fieldname with transforms
#   ./lorem.py dialect+driver://username:password@host:port/database  table.fieldname=transform ...
#   ./lorem.py postgresql:/user:passwd@hostname:5432/mydatabase ...
#   ./lorem.py mysql:/user:passwd@hostname:5432/mydatabase ...
#   ./lorem.py sqlite:////absolute/path/to/foo.db ...
#   ./lorem.py sqlite:///relative/path/to/foo.db  ...

import sys
import logging
from urlparse import urlsplit
from csv import DictReader, DictWriter      # need to do ones with no header line
import sqlite3

from transform import transforms

logging.basicConfig(level=logging.INFO)

# Do CSV first, read from stdin before we worry about arg parsing
# use csv.Sniffer has_header

fields = dict([arg.split(u'=') for arg in sys.argv[2:]])
logging.info(u'fields=%s' % fields)
for transform in fields.values():
    if transform not in transforms:
        raise RuntimeError(u"Requested field name '%s' not in transform names: %s" % (field, transforms.keys()))

source = sys.argv[1]
url = urlsplit(source)
if not url.scheme:              # do a CSV file
    if source == "-":
        csv_in = DictReader(sys.stdin)
        outf = sys.stdout
    else:
        csv_in = DictReader(open(source))
        outf = open("out-%s" % source, "w") # HACK: need to accept an output name
    fieldnames = csv_in.fieldnames
    logging.info(u"csv fieldnames=%s" % fieldnames)
    csv_out = DictWriter(outf, fieldnames)
    for field in fields:
        if field not in fieldnames:
            raise RuntimeError(u"Requested field name '%s' not in CSV fields: %s" % (field, fieldnames))
    csv_out.writeheader()       # not if numeric
    for row in csv_in:
        logging.info(u"row before: %s" % row)
        for field, transform in fields.items():
            row[field] = transforms[transform](row[field])
        logging.info(u"row  after: %s" % row)
        csv_out.writerow(row)

else:                           # do a database
    if not url.scheme.startswith('sqlite'):
        raise RuntimeError(u"We only support sqlite now")
    conn = sqlite3.connect(url.path[1:]) # abs: sqlite3:////path/f.db, rel: sqlite3:///path/f.db
    cursor = conn.cursor()
    # TODO use sqlite3.PARSE_COLNAMES to ensure our field specs are ok
    for field, transform  in fields.items():
        logging.info(u"db field=%s transform=%s" % (field, transform))
        try:
            table, attr = field.split('.')
        except ValueError, e:
            raise RuntimeError(u"Need to specify tablename.attribute separated by a dot in field='%s'" % field)
        # DBAPI doesn't let us do param :name style binding for Table or Column names.
        query = u"SELECT DISTINCT %(attr)s FROM %(table)s" % {'table': table, 'attr': attr}
        cursor.execute(query)
        update = u"UPDATE %(table)s SET %(attr)s = :newvalue WHERE %(attr)s = :value" % {'table': table, 'attr': attr}
        logging.info(u"update: %s" % update)
        for (value,) in cursor.fetchall():
            newvalue = transforms[transform](value)
            #logging.info(u"table=%s attr=%s value=%s newvalue=%s" % (table, attr, value, newvalue))
            cursor.execute(update, {'newvalue': newvalue, 'value': value})
        conn.commit()
