import os
import sys
docroot = os.path.dirname(__file__)
sys.path.append(os.path.join(docroot, "data")) # waar de eigenlijke programmatuur staat
httppad = "http://doctool.pythoneer.nl/"
stylepad = httppad + "style/"
picpad = httppad + "images/"
cgipad = httppad + "cgi-bin/"
htmlpad = '/home/albert/www/pythoneer/doctool'
dtdpad = httppad + "dtd/"
#~ user_xmlpad = docroot + "user/"
#~ func_xmlpad = docroot + "func/"
#~ tech_xmlpad = docroot + "tech/"
#~ proc_xmlpad = docroot + "proc/"
soortfout_html = """\
<html><head></head><body>
Fout in aanroep: je hebt een onjuiste combinatie van hoofd- en<br />
  subcategorie opgegeven<br />
     (de opgegeven waarde was: {}_{})<br />
</body></html>
"""

fouthml = ("""\
<html><head></head><body>
Fout in aanroep: voor de juiste werking moeten de volgende argumenten gevuld zijn:
<br /><br />een hoofdcategorie (user, func, tech of proc)<br />
     (de opgegeven waarde was: {})<br />
<br />een subcategorie (spec, task, proc of data)<br />
     (de opgegeven waarde was: {})<br />
<br />een naam voor de nieuwe specificatie<br />
     (de opgegeven waarde was: {})<br />
<br />en een omschrijving ervoor<br />
     (de opgegeven waarde was: {})<br />
""", '</body></html>')

type_h = ["user","func","tech","proc","project"]
titel_h = ["Gebruikersspecificatie","Functioneel ontwerp","Technisch ontwerp","Bouw","Projecten"]
cat_h = [["spec","docs","wijz"],["docs","task","proc","data"],["task","proc","data"],["proc"],[""]]
cmenu_h = [["lijst gewenste producten","lijst naslag documenten","lijst RFC`s/problemen"],
           ["lijst algemene documenten","lijst gebruikerstaken","lijst functionele processen (invoer, uitvoer of hulp)",
            "datamodel (entiteiten)"],
           ["lijst jobs/transacties","lijst technische processen (programma's/procedures)",
            "datamodel (database, records, files, reports)"],
           ["bouw: lijst programmaspecificaties"],
           ["lijst projectbeschrijvingen"]]
cnieuw_h = [["Nieuwe gebruikersspecificatie","Nieuw naslag document", "Nieuw RFC/probleem"],
            ["Nieuw algemeen document","Nieuwe gebruikerstaak","Nieuw functioneel proces", "Nieuwe entiteit"],
            ["Nieuwe job/transactie", "Nieuw technisch proces", "Nieuwe data-layout"],
            ["Nieuwe programmabeschrijving"],
            ["Nieuwe projectbeschrijving"]]
ctitel_h = [["lijst te maken producten","lijst naslag documenten","lijst RFC`s/problemen"],
            ["lijst algemene documenten","lijst gebruikerstaken","lijst functionele processen","datamodel (entiteiten)"],
            ["lijst jobs/transacties","lijst technische processen","datamodel (records e.d.)"],
            ["lijst programmaspecificaties"],
            ["lijst projectbeschrijvingen"]]
titel_welk = {}
titel_menu = {}
titel_nieuw = {}
titel_list = {}
xmlpad = {} # versie 2: xmlpad = {"index": docroot + "data/"}
typcat = []
#~ t_h = [] # versie 2 : niet (meer) nodig
for x in range(5):
    titel_welk[type_h[x]] = titel_h[x]
    xmlpad[type_h[x]] = docroot + type_h[x] + "/"
    #~ t_h.append(type_h[x][0]) # versie 2 : niet (meer) nodig
    tel = len(cat_h[x])
    for y in range(tel):
        typcat.append(type_h[x] + cat_h[x][y])
        ctype = type_h[x] + "_" + cat_h[x][y]
        if type_h[x] == "project":
            ctype = type_h[x]
        titel_menu[ctype] = cmenu_h[x][y]
        titel_nieuw[ctype] = cnieuw_h[x][y]
        titel_list[ctype] = ctitel_h[x][y]
titel_list["p_egen"] = "lijst E-Gen voorbeeldspecificaties"
titel_list["input"] = "opvoeren/wijzigen specificatie"
