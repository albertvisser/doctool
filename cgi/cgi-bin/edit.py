import cgi
import sys
import globals
sys.path.append(progpad) # waar de eigenlijke programmatuur staat
from edit_main import edit_main

def main():
    form = cgi.FieldStorage()
    form_nok = 0
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
    f = {}
    for x in form.keys():
        f[x] = form[x].value
    e = edit_main(f)
    if e.fout:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        for x in e.regels:
            print x
    else:
        wat = cat = proj = welk = ''
        if form.has_key("hWhat"):
            wat = form["hWhat"].value
        if form.has_key("hCat"):
            cat = form["hCat"].value
        if form.has_key("hProj"):
            proj = form["hProj"].value
        if form.has_key("hWhich"):
            welk = form["hWhich"].value
    #-- terug naar scherm
        print "Content-Type: text/html"     # HTML is following
        print ("Location: %sshow.py?type=item&amp;what=%s&amp;proj=%s&amp;cat=%s&amp;which=%s&amp;edit=1"
                 % (cgipad,wat,proj,cat,welk))
        print                               # blank line, end of headers

if __name__ == '__main__':
	main()
#	test()
