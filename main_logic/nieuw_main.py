# -*- coding: iso-8859-1 -*-
import common
import docobj
from docitems import ItemList, laatste_proj
from relaties import Relaties

fouthtml = """<br/><br/>
de overige argumenten waren - project: {}, van_soort: {}, van_naam: {}<br>
""".join(common.fouthtml)

bestaat_al_html = """\
<html><head></head><body>
De/het opgegeven {}{} bestaat al <br />
     (de opgegeven naam was: {})<br />
</body></html>")
"""
opvoerfout_html = """\
<html><head></head><body>
Fout bij opvoeren nieuwe {}{}:<br />
     {}<br />
     naam was {}<br />
     oms  was {}<br />
     proj was {}<br />
</body></html>
"""

def nieuw(wat, catg, naam, oms, proj, van_soort='', van_naam=''):
    regels = []
    if wat == "" or (wat != "project" and catg == "") or \
            (wat == "project" and catg != "") or \
            naam == "" or oms == "":
        return fouthtml.format(wat, catg, naam, oms, proj,
            van_soort, van_naam), ''
    if van_soort == "item":
        van_soort = ''
    if van_naam == "nieuw":
        van_naam = ''
    ok = True if wat in common.type_h else False
    if ok:
        ok = False if catg not in common.cat_h[i] else True
    if not ok:
       return common.soortfout_html.format((wat,cat))

    if wat == "project":
        catg = ""
        dh = docobj.Project(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.kort = oms
            proj = laatsteproj()
    elif wat == 'user' and catg == 'spec':
        dh = docobj.Userspec(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.kort = oms
    elif wat == 'user' and catg == 'docs':
        dh = docobj.UserDoc(naam, nieuw=True)
        if dh.exists:
            ok = False
    elif wat == 'user' and catg == 'wijz':
        dh = docobj.Userwijz(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.wens = oms
    elif wat == 'func' and catg == 'task':
        dh = docobj.Functask(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.doel = oms
    elif wat == 'func' and catg == 'docs':
        dh = docobj.FuncDoc(naam, nieuw=True)
        if dh.exists:
            ok = False
    elif wat == 'func' and catg == 'proc':
        dh = docobj.Funcproc(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.doel = oms
    elif wat == 'func' and catg == 'data':
        dh = docobj.Entiteit(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.naam = oms
    elif wat == 'tech' and catg == 'proc':
        dh = docobj.Techproc(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.titel = oms
    elif wat == 'tech' and catg == 'task':
        dh = docobj.Techtask(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.kort = oms
    elif wat == 'tech' and catg == 'data':
        dh = docobj.Techdata(naam, nieuw=True)
        if dh.exists:
            ok = False
    elif wat == 'proc' and catg == 'proc':
        dh = docobj.Procproc(naam, nieuw=True)
        if dh.exists:
            ok = False
        else:
            dh.titel = oms
    else:
        return regels("<p>dit zou eigenlijk al eerder afgevangen moeten zijn</p>",
            common.soortfout_html.format(wat,cat))

    if not ok:
        return (bestaat_al_html.format(wat, catg, naam), '')
    else:
        dh.write()
        ih = ItemList(wat + catg, force=True) # force zorgt ervoor dat-ie wordt aangemaakt als-ie er niet is
        if not ih.add_listitem(naam, oms, proj):
            return (opvoerfout_html.format(wat, catg, ih.fout,
                naam, oms, proj), '')
        if van_soort != "" and van_naam != "":
            dh = Relaties(wat + catg, naam)
            # niet lezen, dan blijft alles leeg
            dh.add_relatie(van_soort, van_naam)
            dh.write()
        return ("Location: {}show.py?type=item&amp;what={}&amp;proj={}&amp;"
            "cat={}&amp;which={}&amp;edit=1".format(common.cgipad, wat, proj,
            catg, naam),)
