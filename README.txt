=======
 Lorem
=======

Transform content of CSV and SQL data sources into something innocuous
so that sensitive production data can be used in development, testing,
and demonstrations.

Field Definitions
=================

The user will configure the app by specifying field names and their
types (e.g., text, host name, first name). The code will transform
contents based on type.

Transform Mechanism
===================

In order to preserve consistency in the data, individual fields must
be transformed consistently.  A machine named 'server32' should always
be transformed to a new name such as 'quagmire'. To do this, we'll use
a hash of the source name as an index into a lookup table of target
names.

For plain text, we'll use Lorem Ipsum substitutions.

To preserve shape, we'll replace text with same-sized names and
text: a 100-character text string will be replaced with 100 characters
of Lorem Ipsum text.

Types of Transforms
===================

There are a number of different transforms and to make them easy to
use, they have aliases that should be obvious.

First Name, Last Name, First Last Name, Person Name
---------------------------------------------------

From list of Jazz musicians.  The person_name function looks for a
space and gives only a last name if none found, otherwise and a first
and last name.

Host Name
---------

From list of cocktails (.g., Aviation, Negroni, Martini).

Preserve top level domain (TLD), so *.com stays as *.com.

Transform second level domains into 'example' so foo.nasa.gov becomes foo.example.gov

Transform third level and lower names into themed hostname so
foo.nasa.gov becomes negroni.example.gov and foo.bar.nasa.gov becomes
aviation.negroni.example.gov.

Username
--------

Uses a first-letter + last-name based on the First/Last name
transform.


URL
---

Maintain protocol but transform host name.

Email
-----

Transform username and host name.


Text
----

Lorem Ipsum.

Usage Examples
==============

CSV
---

From named csv, outputs to default out-$SAMENAME::

  ./lorem.py people.csv cn=name sn=name mail=email givenname=name employeenumber=number

SQLite
------

Modifies data in place::

  ./lorem.py sqlite:///people.sqlite people.cn=name people.sn=name people.mail=email people.givenname=name people.employeenumber=number
