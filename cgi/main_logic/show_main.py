# -*- coding: ISO-8859-1 -*-
#-- versie 4
# index op een categorie (welk_categorie.xml) zit in data, de documenten in data\welk_categorie
# de xml parsers voor itemlist, relaties, en de rest allemaal in data
# extra buttons source in toonxml
from doctool_globals import *
from docitems import ItemList
from os.path import exists
from os import getcwd

class show_main:
    def __init__(self,soort,wat,project="0",categorie="",welk="",wijzigstand=False):
        self.form_ok = True
        self.soort = soort
        self.wat = wat
        if project == "": project = "0"
        self.proj = project
        self.cat = categorie
        self.welk = welk
        self.wijzig = wijzigstand
        self.fnaam = ""
        self.zoek = self.wat + "_" + self.cat
        if self.wat == "project": self.zoek = self.wat
        self.lines = []

        if self.soort == "" or self.wat == "":
            self.form_ok = False
        if self.soort != "list" and self.soort != "item":
            self.form_ok = False
        #~ print soort,wat,project,categorie,welk,wijzigstand
        #~ if wat in type_h:
            #~ print "wat in type_h"
        if self.soort != "list" and self.wat != "start" and self.wat not in type_h: #  and self.wat != "nieuw"
            self.form_ok = False
        if self.form_ok:
            #~ print soort,wat,project,categorie,welk,wijzigstand
            self.bepaalfnaam()
        #~ print self.fnaam,self.form_ok,self.htmlofxml
        if self.form_ok:
            self.maakscherm() # was bouw_pagina
        else:
            self.meld_fout()

    def bepaalfnaam(self):
        "bepaal de naam van het bestand op basis waarvan de inhoud voor het gedeelte"
        "'contents' in het template bepaald wordt"
        if self.wijzig:
            self.fnaam = htmlpad + "input_" + self.wat + self.cat + ".html"
        elif self.wat == "start":
            if self.proj == "0":
                self.fnaam = htmlpad + "start_proj_0.html"
            else:
                self.fnaam = htmlpad + "start_proj_other.html"
        elif self.soort == "list":
            self.fnaam = docroot + "data/" + self.wat + "_" + self.cat + ".xml" # bijvoorbeeld ook type=list&what=user&proj=2&cat=spec
        elif self.welk == "nieuw":
            self.fnaam = htmlpad + "nieuw.html"
        else:
            if self.zoek == "":
                self.fnaam = docroot + "data/" + self.wat + ".xml"
            else:
                self.fnaam = docroot + "data/" + self.wat + "_" + self.cat + "/" + self.welk + ".xml"
        self.htmlofxml = self.fnaam[-4:]
        if self.htmlofxml[0] == ".": self.htmlofxml = self.htmlofxml[1:]
        if not exists(self.fnaam):
            form_ok = False

    def meld_fout(self):
        p = file(htmlpad + "err_page.html") # was foutje.html
        for x in p.readlines():
            if x.find("%s") > 0:
                s = x.split("%s")
                if s[1] == "soort":
                    y = ("%s%s%s" % (s[0],self.soort,s[2]))
                elif s[1] == "wat":
                    y = ("%s%s%s" % (s[0],self.wat,s[2]))
                elif s[1] == "proj":
                    y = ("%s%s%s" % (s[0],self.proj,s[2]))
                elif s[1] == "cat":
                    y = ("%s%s%s" % (s[0],self.cat,s[2]))
                elif s[1] == "welk":
                    y = ("%s%s%s" % (s[0],self.welk,s[2]))
                elif s[1] == "fnaam":
                    y = ("%s%s%s" % (s[0],self.fnaam,s[2]))
                else:
                    y = x
                self.lines.append(y[:-1])
            else:
                self.lines.append(x[:-1])
        p.close()

    def maakscherm(self):
        if self.soort == "item" and self.welk != "nieuw" and not self.wijzig:
            # huidige vinden en volgende en vorige bepalen
            self.volgende = ""
            self.vorige = ""
            dh = ItemList(self.wat + self.cat,self.proj) # let op extra argument
            if dh.exists:
                #~ dh.read() #- zit al in __init__
                #~ self.lines.append( ("er zijn %s items in de lijst" % str(dh.aantItems))
                for x in range(dh.aantItems):
                #~ self.lines.append( ('%s heeft index %s in de lijst' % (self.wat,str(x)))
                    if dh.Items[x][0] == self.welk:
                        xp = x - 1
                        if xp >= 0:
                            self.vorige = dh.Items[xp][0]
                        xn = x + 1
                        if xn < dh.aantItems:
                            self.volgende = dh.Items[xn][0]
                        break
        for x in file(htmlpad + "template.html"):
            if x.find('<title>') > -1:
                self.doctitel(x)
            elif x.find('%menu') > -1:
                s = x[:-1].split("%menu")
                self.lines.append(s[0])
                for y in file(htmlpad + "menu.js"):
                    self.lines.append(y[:-1])
                self.lines.append(s[1])
            elif x.find('%start') > -1:
                s = x[:-1].split("%start")
                self.lines.append(s[0])
                for y in file(htmlpad + "start.js"):
                    self.lines.append(y[:-1])
                self.lines.append(s[1])
            elif x.find('</body>') > -1:
                # xhtml plaatje met link naar validator toevoegen
                self.lines.append('<p><br/><br/><br/><a href="http://validator.w3.org/check?uri=referer"><img src="http://www.pythoneer.nl/images/valid-xhtml10" alt="Valid XHTML 1.0!"/></a></p>')
                self.lines.append(x[:-1])
            elif x[0:10] == "<!-- titel":
                self.schermTitel(x)
            elif x.find("menu") > -1:
                s = x.split("$$")
                self.lines.append(s[0])
                self.schermMenu()
                self.lines.append(s[1])
            elif x.find("begin") > -1:
                s = x.split("$$")
                if self.soort == "list" and self.wat != "start": # op het startscherm geen linkerkolom
                    self.lines.append(s[1])
                    self.lines.append(s[2] % "kw3")
                else:
                    self.lines.append(s[2] % "full")
            elif x.find("iframe") > -1: # contents
                self.schermContent()
            elif x.find("eind") > -1:
                s = x.split("$$")
                self.lines.append(s[1][:-1])
                if self.wijzig:
                    self.lines.append('     <span style="width: 10%; float:left; ">&nbsp;</span>')
            else:
                self.lines.append(x[:-1])

    def doctitel(self,x):
        "bepaal de titel van het html document (in de heading)"
        h = x[:-1].split("%s")
        if self.wat == "start":
            s = self.wat
            if self.proj != "" and self.proj != "0":
                s = "project " + s
        elif self.welk == "nieuw":
            s = "nieuw " + self.wat + self.cat
        else:
            s = self.wat + self.cat + " " + self.soort
        self.lines.append(s.join(h))

    def schermTitel(self,x):
        "bepaal de titel van de pagina op het scherm"
        t = ""
        if self.soort == "list":
            if self.wat == "start":
                t = "Welcome to DocTool!"
                if self.proj != "" and self.proj != "0":
                    t = "Project startpagina"
            else:
                if self.wat == "input":
                    h = self.wat
                else:
                    h = self.wat + "_" + self.cat
                t = titel_list[h].capitalize()
        elif self.soort == "item":
            h = self.zoek
            if self.welk == "nieuw":
                t = titel_nieuw[h]
            else:
                s = titel_nieuw[h].split()
                t0 = s[1].capitalize()
                t1 = ""
                if len(s) == 3:
                    t1 = " " + s[2]
                t2 = ": " + self.welk.capitalize()
                t = ("%s%s%s"  % (t0,t1,t2))
        self.lines.append(t)

    def schermMenu(self):
        for y in file(htmlpad + "menu.html"):
            y = y[:-1]
            if y.find("Home") >= 0 :
                pass
            elif y.find("Top") >= 0 and self.soort != "item":
                continue # y = ''
            elif y.find("Nieuw") >= 0:
                if self.wat == "start":
                    if self.proj == "0":
                        y = y.replace("%wat","project")
                        y = y.replace("%s","Nieuw project")
                    else:
                        continue # y = y.replace("%s","Nieuwe %wat%cat")
                else:
        #~ http://doctool.pythoneer.nl/cgi-bin/show.py?type=item&what=project&proj=5&cat=&which=&edit=1
                    if self.welk == "nieuw" or (self.welk == "" and self.soort !="list"):
                        continue # y = ''
                    else:
                        y = y.replace("%s","Nieuwe %wat%cat")
            elif y.find("Vorige") >= 0:
                if not self.wijzig and self.soort == "item" and self.welk != "nieuw" and self.vorige != "":
                    y = y.replace("%vorige",self.vorige)
                else:
                    continue # y = ''
            elif y.find("Volgende") >= 0:
                if not self.wijzig and self.soort == "item" and self.welk != "nieuw" and self.volgende != "":
                    y = y.replace("%volgende",self.volgende)
                else:
                    continue # y = ''
            elif y.find("Wijzig") >= 0:
                if self.wijzig:
                    continue # y = ''
                elif self.soort == "item" and self.welk != "nieuw":
                    pass
                elif self.wat == "start" and self.proj != "0":
                    y = y.replace("%wat","project")
                    y = y.replace("%cat","")
                    y = y.replace("%welk","")
                else:
                    y = ''
            elif y.find("Bekijk") >= 0:
                if not self.wijzig:
                    continue
                elif self.welk == "":  #~ http://doctool.pythoneer.nl/cgi-bin/show.py?type=item&what=project&proj=5&cat=&which=&edit=1
                    y = y.replace("item","list")
                    y = y.replace("%wat","start")
                #~ if self.soort == "item" and self.welk != "nieuw":
                    #~ y = ''
                #~ elif self.wat == "start" and self.proj != "0":
                    #~ y = ''
                #~ else:
                    #~ pass
            elif (self.wat == "start" or self.cat == "wijz") and self.proj == "0" and y.find("<li><a") >= 0 :
                continue # y = ''
            y = y.replace("%cgipad",cgipad)
            y = y.replace("%wat",self.wat)
            y = y.replace("%proj",self.proj)
            y = y.replace("%cat",self.cat)
            y = y.replace("%welk",self.welk)
            if y != '':
                self.lines.append(y)

    def schermContent(self):
        "inhoud samenstellen van het menu- of gegevensgedeelte"
        self.lines.append('<span style="width: 100%; height: 600px; overflow: auto">')
        if self.soort == "item" and self.welk != "nieuw" and not self.wijzig:
            di = ItemList("project")
            #~ di.read() #- zit al in __init__
            p = di.Items[int(self.proj)]
            self.lines.append('<span class="headr">Hoort bij project: <a href="%sshow.py?type=list&amp;what=start&amp;proj=%s">%s</a></span><br/>' % (cgipad,p[0],p[1]))
        if self.htmlofxml == "html": # start, nieuw of item in wijzigstand: contents begint/eindigt met html stuk
            from printobject import printHTMLObject
            self.printh = printHTMLObject(self)
            for x in self.printh.lines:
                self.lines.append(x)
        else: # self.soort == "item" and self.welk != "nieuw":
            from printobject import printXMLObject
            self.printh = printXMLObject(self)
            for y in self.printh.regels:
                self.lines.append(y)
        if self.wat == "start" and self.proj == "0":
            for x in file(htmlpad + "browser.html"):
                self.lines.append(x)
        self.lines.append('</span>')

def test():
    #~ http://doctool.pythoneer.nl/cgi-bin/show.py?type=item&what=user&proj=27&cat=docs&which=lifecycle
    # startscherm:              type=list&what=start                        ok
    # startscherm project       type=list&what=start&proj=1                 ok
    # RFC's alle projecten      type=list&what=user&proj=0&cat=wijz         ok
    # overzicht rfc per project type=list&what=user&proj=1&cat=wijz         ok
    # overzicht userdocs        type=list&what=user&proj=27&cat=docs        ok
    # overzicht userspecs       type=list&what=user&proj=1&cat=spec         ok
    # overzicht funcdocs        type=list&what=func&proj=27&cat=docs        ok
    # overzicht functask        type=list&what=func&proj=1&cat=task         ok
    # overzicht funcproc        type=list&what=func&proj=1&cat=proc         ok
    # overzicht funcdata        type=list&what=func&proj=1&cat=data         ok
    # overzicht techtask        type=list&what=tech&proj=1&cat=task         ok
    # overzicht techproc        type=list&what=tech&proj=1&cat=proc         ok
    # overzicht techdata        type=list&what=tech&proj=1&cat=data         ok
    # overzicht procs           type=list&what=proc&proj=1&cat=proc         ok
    # document r/o              type=item&what=func&proj=1&cat=task&which=Docspec           ok
    # document r/o              type=item&what=func&proj=27&cat=docs&which=inleiding        ok
    # document r/o              type=item&what=user&proj=27&cat=docs&which=lifecycle        ok
    # idem wijzigen             type=item&what=func&proj=1&cat=task&which=Docspec&edit=1    ok
    # idem wijzigen             type=item&what=func&proj=27&cat=docs&which=inleiding&edit=1 ok
    # nieuwe rfc                type=item&what=user&proj=0&cat=wijz&which=nieuw             ok
    # nieuwe rfc bij project    type=item&what=user&proj=1&cat=wijz&which=nieuw             ok
    # nieuw item                type=item&what=func&proj=1&cat=task&which=nieuw             ok
    # nieuw project             type=item&what=project&proj=0&cat=&which=nieuw              ok
    soort = "item"            # list of item
    wat = "project"             # start, user, func, tech, proc - nieuw? input?
    project =  "0"             # volgnummer
    categorie = ""            # spec, wijz, task, proc, data
    welk = "nieuw"                 # naam of "nieuw"
    wijzigstand = False  # True or False
    l = show_main(soort,wat,project,categorie,welk,wijzigstand)
    #~ f = file(("%stest_%s%s%s_%s_%s.html" % (htmlpad,soort,wat,categorie,project,welk)),"w")
    f = file("test.html","w")
    for x in l.lines:
      f.write("%s\n" % x)
    f.close()

if __name__ == '__main__':
    test()
