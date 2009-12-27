import cgi
import sys
import globals
sys.path.append(progpad) # waar de eigenlijke programmatuur staat
from nieuw_main import nieuw_main

def main():
    form = cgi.FieldStorage()
    # print "Content-Type: text/html"     # HTML is following
    # print                               # blank line, end of headers
    # print "<html>"
    # print "<head></head>"
    # print "<body>"
    # keys = form.keys()
    # keys.sort()
    # print
    # print "<H3>Form Contents:</H3>"
    # if not keys:
        # print "<P>No form fields."
    # print "<DL>"
    # for key in keys:
        # print "<DT>" + cgi.escape(key) + ":",
        # value = form[key]
        # print "<i>" + cgi.escape(`type(value)`) + "</i>"
        # print "<DD>" + cgi.escape(`value`)
    # print "</DL>"
    # print
    # print "</body></html>"
    # return

    #~ # zelf argumenten instellen
    #~ proj = "28"
    #~ catg = "spec"
    #~ wat = "user"
    #~ vanSoort = "item"
    #~ vanNaam = "nieuw"
    #~ naam = "Basis"
    #~ oms = "Basis vormgeving en navigatie"

    #-- argumenten lezen
    if form.has_key("hProj"):
        proj = form["hProj"].value
    else:
        if form.has_key("proj"):
            proj = form["hProj"].value
        else:
            proj = ""
    #   hWat en hCat geven aan wat voor nieuw item het om gaat
    if form.has_key("hWat"):
        wat = form["hWat"].value
    else:
        wat = ""
    if form.has_key("hCat"):
        catg = form["hCat"].value
    else:
        catg = ""

    # naam en omschrijving zijn al opgegeven, als het goed is
    if form.has_key("txtNaam"):
        naam = form["txtNaam"].value
    else:
        naam = ""
    if form.has_key("txtOms"):
        oms = form["txtOms"].value
    else:
        oms = ""

    #   als vanuit een ander soort item wordt opgevoerd, worden hType en hName meegegeven
    #   hier moet een relatie naar gemaakt worden
    vanSoort = ""
    vanNaam = ""
    if form.has_key("hType"):
        vanSoort = form["hType"].value
    if form.has_key("hName"):
        vanNaam = form["hName"].value

    r = nieuw_main(wat,catg,naam,oms,proj,vanSoort,vanNaam)
    print "Content-Type: text/html"     # HTML is following
    if len(r.regels) == 1:
        print r.regels[0]                   # doorverwijzing naar edit scherm
        print                               # blank line, end of headers
    elif len(r.regels) > 0:
        print                               # blank line, end of headers
        for l in r.regels:
            print l

if __name__ == '__main__':
   main()
