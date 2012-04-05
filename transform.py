# -*- encoding: utf-8 -*-
import md5
from urlparse import urlsplit, urlunsplit

# Import under different names for easy reference and trivial substitution later.

from cocktails import names as hostnames
from jazz import names as first_last
from text import text as replacement_text

def select(text, candidates):
    """Return entry from candidates based on hash of text.
    This is probably unnecessarily slow.
    """
    m = md5.new()
    m.update(text)
    hexnum = m.hexdigest()
    decnum = int(hexnum, 16)
    index = decnum % len(candidates)
    return candidates[index]

def host_name(name):
    """Replace a simple hostname or a FQDN, preserving the TLD.
    """
    if name.strip() == "":
        return name
    fqdn = name.split('.')
    if len(fqdn) == 0:
        logging.warning("hostname empty")
        return ""
    if len(fqdn) == 1:
        return select(fqdn[0], hostnames).lower()
    fqdn[-2] = 'example'
    for n in range(0, len(fqdn) - 2):
        fqdn[n] = select(fqdn[n], hostnames)
    return '.'.join(fqdn).lower()

def first_last_name(name):
    if name.strip() == "":
        return name
    return ' '.join(select(name, first_last))

def first_name(name):
    if name.strip() == "":
        return name
    return select(name, first_last)[0]

def last_name(name):
    if name.strip() == "":
        return name
    return select(name, first_last)[1]

def person_name(name):
    """Return a full name or last name.
    """
    if name.strip() == "":
        return name
    if ' ' in name:
        return first_last_name(name)
    else:
        return last_name(name)

def url(name):
    """Keep method, path, query, but replace hostname.
    """
    if name.strip() == "":
        return name
    (scheme, netlock, path, query, fragment) = urlsplit(name)
    netlock = host_name(netlock)
    return urlunsplit((scheme, netlock, path, query, fragment))

def ip(name):
    """Return an RFC1918 address so we don't point at legit machines.
    """
    if name.strip() == "":
        return name
    m = md5.new()
    m.update(name)
    h = m.hexdigest()
    return '10.' + '.'.join(["%d" % int(h[i:i+2], 16) for i in [2, 4, 6]])

def username(name):
    """Map usernames to downcase so different cases give same result.
    """
    if name.strip() == "":
        return name
    first, last = select(name.lower(), first_last)
    return first[0] + last

def email(address):
    if address.strip() == "":
        return address
    (u, h) = address.split('@')
    return "@".join((username(u), host_name(h)))

def text(text):
    """
    TODO:
    - text longer than sample
    - pseudo random repeatable
    """
    if text.strip() == "":
        return text
    return replacement_text[:len(text)]





