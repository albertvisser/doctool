#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import sys
from codecs import getwriter
sys.stdout = getwriter("utf-8")(sys.stdout.buffer)
import doctool_globals
from show_main import Show

def main():
    form = cgi.FieldStorage()
    soort = form.getfirst("type", "")
    wat = form.getfirst("what", "")
    project = form.getfirst("proj", "0")
    categorie = form.getfirst("cat", "")
    welk = form.getfirst("which", "")
    edit = True if "edit" in form else False
    print("Content-Type: text/html\n")     # HTML is following
    l = Show(soort, wat, project, categorie, welk, edit)
    for x in l.lines:
        print(x)

if __name__ == '__main__':
    main()
