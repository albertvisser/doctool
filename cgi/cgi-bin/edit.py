#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import doctool_globals
from edit_main import edit

def main():
    form = cgi.FieldStorage()
    form_nok = 0
    fout, regels = edit({x: form.getfirst(x) for x in form.keys()})
    if fout:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        for x in regels:
            print x
    else:
        wat  = form.getfirst("hWhat", '')
        cat  = form.getfirst("hCat", '')
        proj = form.getfirst("hProj", '')
        welk = form.getfirst("hWhich", '')
    #-- terug naar scherm
        print "Content-Type: text/html"     # HTML is following
        print ("Location: {}show.py?type=item&amp;what={}&amp;proj={}"
                "&amp;cat={}&amp;which={}&amp;edit=1".format(
                doctool_globals.cgipad, wat, proj, cat, welk))
        print                               # blank line, end of headers

if __name__ == '__main__':
  	main()
