# -*- coding: iso-8859-1 -*-

from doctool_globals import *

class nieuw_main:
    def __init__(self,wat,catg,naam,oms,proj,vanSoort='',vanNaam=''):
        self.regels = []

        if wat == "" or (wat != "project" and catg == "") or naam == "" or oms == "":
            #~ self.regels.append("Content-Type: text/html")     # HTML is following
            #~ self.regels.append("")                            # blank line, end of headers
            self.regels.append("<html>")
            self.regels.append("<head></head>")
            self.regels.append("<body>")
            self.regels.append("Fout in aanroep: voor de juiste werking moeten de volgende argumenten gevuld zijn:<br />")
            self.regels.append("<br />")
            self.regels.append("een hoofdcategorie (user, func, tech of proc)<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % wat)
            self.regels.append("<br />")
            self.regels.append("een subcategorie (spec, task, proc of data)<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % catg)
            self.regels.append("<br />")
            self.regels.append("een naam voor de nieuwe specificatie<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % naam)
            self.regels.append("<br />")
            self.regels.append("en een omschrijving ervoor<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % oms)
            self.regels.append('<br/><br/>')
            self.regels.append('de overige argumenten waren - project: %s ,vanSoort: %s , vanNaam: %s<br>' % (proj,vanSoort,vanNaam))
            self.regels.append("</body></html>")
            return
        if vanSoort == "item": vanSoort = ''
        if vanNaam == "nieuw": vanNaam = ''
        ok = True
        try:
            i = type_h.index(wat)
        except:
            ok = False
        if ok:
            try:
                j = cat_h[i].index(catg)
            except:
                ok = False
        if not ok:
            #~ self.regels.append("Content-Type: text/html")     # HTML is following
            #~ self.regels.append("")                            # blank line, end of headers
            self.regels.append("<html>")
            self.regels.append("<head></head>")
            self.regels.append("<body>")
            self.regels.append("Fout in aanroep: je hebt een onjuiste combinatie van hoofd- en<br />")
            self.regels.append("  subcatg opgegeven<br />")
            self.regels.append("     (de opgegeven waarde was: %s_%s)<br />" % (wat,catg))
            self.regels.append("</body></html>")
            return

        if wat == "project":
            from project import Project
            dh = Project("0")
            proj = dh.Id
            dh.setAttr("naam",naam)
            dh.setAttr("kort",oms)
        elif wat == 'user' and catg == 'spec':
            from userspec import Userspec
            dh = Userspec(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigKort(oms)
        elif wat == 'user' and catg == 'docs':
            from userdocs import UserDoc
            dh = UserDoc(naam,nieuw=True)
            if dh.exists:
                ok = False
        elif wat == 'user' and catg == 'wijz':
            from userwijz import Userwijz
            dh = Userwijz(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigWens(oms)
        elif wat == 'func' and catg == 'docs':
            from funcdocs import FuncDoc
            dh = FuncDoc(naam,nieuw=True)
            if dh.exists:
                ok = False
        elif wat == 'func' and catg == 'task':
            from functask import Functask
            dh = Functask(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigDoel(oms)
        elif wat == 'func' and catg == 'proc':
            from funcproc import Funcproc
            dh = Funcproc(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigDoel(oms)
        elif wat == 'func' and catg == 'data':
            from funcdata import Entiteit
            dh = Entiteit(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigNaam(oms)
        elif wat == 'tech' and catg == 'proc':
            from techproc import Techproc
            dh = Techproc(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigTitel(oms)
        elif wat == 'tech' and catg == 'task':
            from techtask import Techtask
            dh = Techtask(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigKort(oms)
        elif wat == 'tech' and catg == 'data':
            from techdata import Techdata
            dh = Techdata(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                pass
        elif wat == 'proc' and catg == 'proc':
            from procproc import Procproc
            dh = Procproc(naam,nieuw=True)
            if dh.exists:
                ok = False
            else:
                dh.wijzigTitel(oms)
        else:
            ok = False

        if not ok:
            #~ self.regels.append("Content-Type: text/html")     # HTML is following
            #~ self.regels.append("")                            # blank line, end of headers
            self.regels.append("<html>")
            self.regels.append("<head></head>")
            self.regels.append("<body>")
            self.regels.append("De/het opgegeven %s%s bestaat al <br />" % (wat,catg))
            self.regels.append("     (de opgegeven naam was: %s)<br />" % (naam))
            self.regels.append("</body></html>")
            return
        else:
            dh.write()
            if wat != "project":
                from docitems import ItemList
                ih = ItemList(wat + catg,force=True) # force zorgt ervoor dat-ie wordt aangemaakt als-ie er niet is
                #~ ih.read() #- zit al in __init__
                if not ih.addListItem(naam,oms,proj):
                    self.regels.append("<html>")
                    self.regels.append("<head></head>")
                    self.regels.append("<body>")
                    self.regels.append("Fout bij opvoeren nieuwe %s%s:<br />" % (wat,catg))
                    self.regels.append("     %s<br />" % (ih.fout))
                    self.regels.append("     naam was %s<br />" % (naam))
                    self.regels.append("     oms  was %s<br />" % (oms))
                    self.regels.append("     proj was %s<br />" % (proj))
                    self.regels.append("</body></html>")
                    return
                ih.write()
            #-- relatie naar het document vanuit welk dit wordt opgevoerd leggen
                if vanSoort != "" and vanNaam != "":
                    from relaties import Relaties
                    dh = Relaties(wat+catg,naam)
                    # niet lezen, dan blijft alles leeg
                    dh.addRelatie(vanSoort,vanNaam)
                    dh.write()

        #-- door naar editscherm
            #~ self.regels.append("Content-Type: text/html")     # HTML is following
            self.regels.append("Location: %sshow.py?type=item&amp;what=%s&amp;proj=%s&amp;cat=%s&amp;which=%s&amp;edit=1"
                 % (cgipad,wat,proj,catg,naam))
            #~ self.regels.append("")                              # blank line, end of headers

def test():
    # nieuw project: hProj=0&hWat=project&hType=item&hName=nieuw&txtNaam=Iets&txtOms=Meer
    # nieuw iets anders: hProj=1&hCat=proc&hWat=func&hType=item&hName=nieuw&txtNaam=&txtOms=
    wat = "project"
    catg = ""
    naam = "validatie"
    oms = "vooraf controleren of er gemigreerd mag worden"
    proj = "0"
    vanSoort = "item"
    vanNaam = "nieuw"
    r = nieuw_main(wat,catg,naam,oms,proj,vanSoort,vanNaam)
    f = file(("test_nieuw_%s%s.html" % (wat,catg)),"w")
    for l in r.regels:
        f.write("%s\n" % l)
    f.close()

if __name__ == '__main__':
    test()
