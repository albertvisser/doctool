#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""\
hWat en hCat geven aan wat voor nieuw item het om gaat
naam en omschrijving zijn al opgegeven, als het goed is
  als vanuit een ander soort item wordt opgevoerd, worden hType en hName meegegeven
  hier moet een relatie naar gemaakt worden
"""
import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import doctool_globals
from nieuw_main import nieuw

def main():
    form = cgi.FieldStorage()
    proj = form.getfirst("hProj", "")
    if not proj:
        proj = form.getfirst("hProj", "")
    wat = form.getfirst("hWat", "")
    catg = form.getfirst("hCat", "")
    naam = form.getfirst("txtNaam", "")
    oms = form.getfirst("txtOms", "")
    van_soort = form.getfirst("hType", "")
    van_naam = form.getfirst("hName", "")
    regels = nieuw(wat, catg, naam, oms, proj, van_soort, van_naam)
    print("Content-Type: text/html")
    if len(regels) == 1:
        print(regels[0])
        print()
    elif len(regels) > 0:
        print()
        for l in regels:
            print(l)

if __name__ == '__main__':
   main()
