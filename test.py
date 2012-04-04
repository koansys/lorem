#!/usr/bin/env python
# -*- encode: utf-8 -*-

import unittest

import transform as t

class TestSelect(unittest.TestCase):

    def test_a(self):
        self.assertEqual(t.select('a', [1,2]), 2)

    def test_b(self):
        self.assertEqual(t.select('b', [1,2]), 2)

    def test_e(self):
        self.assertEqual(t.select('e', [1,2]), 1)

class TestHostName(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(t.host_name(''), '')

    def test_no_domain_1(self):
        self.assertEqual(t.host_name('foo'), 'royce')

    def test_no_domain(self):
        self.assertEqual(t.host_name('bar'), 'earthquake')

    def test_domain_tld(self):
        self.assertEqual(t.host_name('foo.gov'), 'example.gov')

    def test_host_domain(self):
        self.assertEqual(t.host_name('foo.bar.com'), 'royce.example.com')

    def test_host_domain_2(self):
        self.assertEqual(t.host_name('foo.bar.stuff.gov'), 'royce.earthquake.example.gov')

class TestFirstLastName(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(t.first_last_name(""), '')

    def test_firstname_only(self):
        self.assertEqual(t.first_last_name("Joe"), 'Charlie Christian')

    def test_first_and_last(self):
        self.assertEqual(t.first_last_name("Joe Smith"), 'Nick LaRocca')

class TestFirstName(unittest.TestCase):

    def test_empt(self):
        self.assertEqual(t.first_name(""), '')

    def test_first(self):
        self.assertEqual(t.first_name("Joe"), 'Charlie')

    def test_first_last(self):
        self.assertEqual(t.first_name("Joe Smith"), 'Nick')

class TestLastName(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(t.last_name(""), '')

    def test_last_only(self):
        self.assertEqual(t.last_name("Smith"), 'Davis')

    def test_first_last(self):
        self.assertEqual(t.last_name("Joe Smith"), 'LaRocca')

class TestPersonName(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(t.person_name(""), '')

    def test_first_only(self):
        self.assertEqual(t.person_name("Joe"), 'Christian')

    def test_first_only_2(self):
        self.assertEqual(t.person_name("Smith"), 'Davis')

    def test_first_last(self):
        self.assertEqual(t.person_name("Joe Smith"), 'Nick LaRocca')

    def test_first_m_last(self):
        self.assertEqual(t.person_name("Joe Q Smith"), 'Herbie Hancock')

class TestUrl(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(t.url(""), '')

    def test_host_tld(self):
        self.assertEqual(t.url("http://foo.com"), 'http://example.com')

    def test_host_tld_ftp(self):
        self.assertEqual(t.url("ftp://foo.com"), 'ftp://example.com')

    def test_host_domain(self):
        self.assertEqual(t.url("https://foo.bar.com"), 'https://royce.example.com')

    def test_host_domain_path(self):
        self.assertEqual(t.url("https://foo.bar.stuff.com/path/to/thing?query=42#pound"),
                         'https://royce.earthquake.example.com/path/to/thing?query=42#pound')

class TestIp(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(t.ip(""), '')

    def test_ip_1(self):
        self.assertEqual(t.ip("192.168.1.2"), '10.18.15.243')

    def test_ip_2(self):
        self.assertEqual(t.ip("172.16.1.2"), '10.46.239.164')

class TestUsername(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(t.username(""), '')

    def test_lower(self):
        self.assertEqual(t.username("jsmith"), 'JPonty')

    def test_upper(self):
        self.assertEqual(t.username("JSMITH"), 'JPonty')

    def test_username(self):
        self.assertEqual(t.username("jsmith1"), 'TPitts')

class TestEmail(unittest.TestCase):

    def test_email(self):
        self.assertEqual(t.email("jsmith@example.gov"), 'JPonty@example.gov')

    def test_email_1(self):
        self.assertEqual(t.email("jsmith1@example.gov"), 'TPitts@example.gov')

    def test_email_fqdn(self):
        self.assertEqual(t.email("jsmith1@foo.example.gov"), 'TPitts@royce.example.gov')

class TestText(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
