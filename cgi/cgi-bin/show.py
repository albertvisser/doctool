# -*- coding: ISO-8859-1 -*-
import cgi
import sys
from globals import *
sys.path.append(progpad) # waar de eigenlijke programmatuur staat
from show_main import show_main

def main():
    form = cgi.FieldStorage()
    #~ print "Content-Type: text/html"     # HTML is following
    #~ print                               # blank line, end of headers
    #~ print "<html>"
    #~ print "<head></head>"
    #~ print "<body>"
    #~ keys = form.keys()
    #~ keys.sort()
    #~ print
    #~ print "<H3>Form Contents:</H3>"
    #~ if not keys:
        #~ print "<P>No form fields."
    #~ print "<DL>"
    #~ for key in keys:
        #~ print "<DT>" + cgi.escape(key) + ":",
        #~ value = form[key]
        #~ print "<i>" + cgi.escape(`type(value)`) + "</i>"
        #~ print "<DD>" + cgi.escape(`value`)
    #~ print "</DL>"
    #~ print
    #~ print "</body></html>"
    #~ return
    #~ soort = "item"
    #~ wat = "user"
    #~ project = "28"
    #~ categorie = "spec"
    #~ welk = "nieuw"
    #~ edit = False
    #-- argumenten lezen
    if form.has_key("type"):
        soort = form["type"].value
    else:
        soort = ""
    if form.has_key("what"):
        wat = form["what"].value
    else:
        wat = ""
    if form.has_key("proj"):
        project = form["proj"].value
    else:
        project = "0"
    if form.has_key("cat"):
        categorie = form["cat"].value
    else:
        categorie = ""
    if form.has_key("which"):
        welk = form["which"].value
    else:
        welk = ""
    if form.has_key("edit"):
        edit = True
    else:
        edit = False
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    #~ print "<html>"
    #~ print "<head></head>"
    #~ print "<body>"
    #~ print "de argumenten waren:"
    #~ print "<dl>"
    #~ print (" <dt>soort:</dt><dd>%s</dd>" % soort)
    #~ print (" <dt>wat:</dt><dd>%s</dd>" % wat)
    #~ print (" <dt>project:</dt><dd>%s</dd>" %project)
    #~ print (" <dt>cat:</dt><dd>%s</dd>" % categorie)
    #~ print (" <dt>welk:</dt><dd>%s</dd>" % welk)
    #~ print (" <dt>edit:</dt><dd>%s</dd>" % edit)
    #~ print "</dl>"
    #~ print "Dus de aanroep van het vervolg wordt:<br />"
    #~ print ('<br />lines = show_main("%s","%s","%s","%s","%s","%s")' % (soort,wat,project,categorie,welk,edit))
    #~ print "</body></html>"
    #~ return
    l = show_main(soort,wat,project,categorie,welk,edit)
    for x in l.lines:
        print x

if __name__ == '__main__':
    main()
