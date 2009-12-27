httppad = "http://doctool.pythoneer.nl/"
htmlpad = "f:/www/pythoneer/DocTool/"
stylepad = httppad + "style/"
picpad = httppad + "images/"
cgipad = httppad + "cgi-bin/"
docroot = "F:\\pythoneer\\doctool\\"
dtdpad = httppad + "dtd/"
#~ user_xmlpad = docroot + "user/"
#~ func_xmlpad = docroot + "func/"
#~ tech_xmlpad = docroot + "tech/"
#~ proc_xmlpad = docroot + "proc/"
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

import sys
sys.path.append(docroot + "data") # waar de eigenlijke programmatuur staat