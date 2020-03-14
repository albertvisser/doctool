# -*- coding: ISO-8859-1 -*-
#-- versie 4
# index op een categorie (welk_categorie.xml) zit in data, de documenten in data\welk_categorie
# de xml parsers voor itemlist, relaties, en de rest allemaal in data
# extra buttons source in toonxml
import os
import common
from docitems import ItemList
from printobject import PrintHTMLObject, PrintXMLObject

class Show:
    def __init__(self, soort, wat, project="0", categorie="", welk="",
            wijzigstand=False):
        self.form_ok = True
        self.soort = soort
        self.wat = wat
        if project == "":
            project = "0"
        self.proj = project
        self.cat = categorie
        self.welk = welk
        self.wijzig = wijzigstand
        self.fnaam = ""
        self.zoek = self.wat + "_" + self.cat
        if self.wat == "project":
            self.zoek = self.wat
        self.lines = []

        if self.soort == "" or self.wat == "":
            self.form_ok = False
        if self.soort != "list" and self.soort != "item":
            self.form_ok = False
        #~ print soort,wat,project,categorie,welk,wijzigstand
        #~ if wat in type_h:
            #~ print "wat in type_h"
        if self.soort != "list" and self.wat != "start" \
                and self.wat not in common.type_h:
            #  and self.wat != "nieuw"
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
        """bepaal de naam van het bestand op basis waarvan de inhoud voor het
        gedeelte 'contents' in het template bepaald wordt"""
        if self.wijzig:
            self.fnaam = os.path.join(common.htmlpad,
                "input_{}{}.html".format(self.wat, self.cat))
        elif self.wat == "start":
            text = "other" if self.proj != "0" else "0"
            self.fnaam = os.path.join(common.htmlpad,
                "start_proj_{}.html".format(text))
        elif self.soort == "list":
            self.fnaam = os.path.join(common.docroot, "data",
                 "{}_{}.xml".format(self.wat, self.cat)) # bijvoorbeeld ook type=list&what=user&proj=2&cat=spec
        elif self.welk == "nieuw":
            self.fnaam = os.path.join(common.htmlpad, "nieuw.html")
        elif self.zoek == "":
            self.fnaam = os.path.join(common.docroot, "data",
                "{}.xml".format(self.wat))
        else:
            self.fnaam = os.path.join(common.docroot, "data",
                '{}_{}'.format(self.wat, self.cat),
                "{}.xml".format(self.welk.lower()))
        self.htmlofxml = os.path.splitext(self.fnaam)[1][1:]
        if not os.path.exists(self.fnaam):
            form_ok = False

    def meld_fout(self):
        with open(os.path.join(common.htmlpad, "err_page.html")) as p:
            for x in p:
                y = x
                if "%s" in x:
                    s = x.split("%s")
                    if s[1] == "soort":
                        y = ("%s%s%s" % (s[0],self.soort,s[2]))
                        # y = y.replace(s[1], self.soort)
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
                self.lines.append(y.strip())

    def maakscherm(self):
        if self.soort == "item" and self.welk != "nieuw" and not self.wijzig:
            # huidige vinden en volgende en vorige bepalen
            self.volgende = ""
            self.vorige = ""
            dh = ItemList(self.wat + self.cat, self.proj) # let op extra argument
            if dh.exists:
                #~ self.lines.append( ("er zijn %s items in de lijst" % str(dh.aantItems))
                for x in range(dh.aant_items):
                #~ self.lines.append( ('%s heeft index %s in de lijst' % (self.wat,str(x)))
                    if dh.items[x][0] == self.welk:
                        xp = x - 1
                        if xp >= 0:
                            self.vorige = dh.items[xp][0]
                        xn = x + 1
                        if xn < dh.aant_items:
                            self.volgende = dh.items[xn][0]
                        break
        with open(os.path.join(common.htmlpad, "template.html")) as f:
            for x in f:
                x = x.rstrip()
                if '<title>' in x:
                    self.doctitel(x)
                elif '%menu' in x:
                    s = x.split("%menu")
                    self.lines.append(s[0])
                    with open(os.path.join(common.htmlpad, "menu.js")) as f:
                        self.lines.extend([y.lstrip() for y in f])
                    self.lines.append(s[1])
                elif '%start' in x:
                    s = x.split("%start")[:-1]
                    self.lines.append(s[0])
                    with open(os.path.join(common.htmlpad, "start.js")) as f:
                        self.lines.append([y.lstrip() for y in f])
                    self.lines.append(s[1])
                ## elif '</body>' in x:
                    ## # xhtml plaatje met link naar validator toevoegen
                    ## self.lines.append('<p><br/><br/><br/>'
                        ## '<a href="http://validator.w3.org/check?uri=referer">'
                        ## '<img src="/images/valid-xhtml10"'
                        ## ' alt="Valid XHTML 1.0!"/></a></p>')
                    ## self.lines.append(x)
                elif x.startswith("<!-- titel"):
                    self.scherm_titel(x)
                elif "menu" in x:
                    s = x.split("$$")
                    self.lines.append(s[0])
                    self.scherm_menu()
                    self.lines.append(s[1])
                elif "begin" in x:
                    s = x.split("$$")
                    if self.soort == "list" and self.wat != "start": # op het startscherm geen linkerkolom
                        self.lines.append(s[1])
                        self.lines.append(s[2] % "kw3")
                    else:
                        self.lines.append(s[2] % "full")
                elif "iframe" in x: # contents
                    self.scherm_content()
                elif "eind" in x:
                    s = x.split("$$")
                    self.lines.append(s[1])
                    if self.wijzig:
                        self.lines.append('     <span style="width: 10%;'
                            ' float:left; ">&nbsp;</span>')
                else:
                    self.lines.append(x)

    def doctitel(self, x):
        "bepaal de titel van het html document (in de heading)"
        if self.wat == "start":
            s = self.wat
            if self.proj != "" and self.proj != "0":
                s = "project " + s
        elif self.welk == "nieuw":
            s = "nieuw " + self.wat + self.cat
        else:
            s = self.wat + self.cat + " " + self.soort
        self.lines.append(x % s)

    def scherm_titel(self,x):
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
                t = common.titel_list[h].capitalize()
        elif self.soort == "item":
            h = self.zoek
            if self.welk == "nieuw":
                t = common.titel_nieuw[h]
            else:
                s = common.titel_nieuw[h].split()
                t0 = s[1].capitalize()
                t1 = ""
                if len(s) == 3:
                    t1 = " " + s[2]
                t2 = ": " + self.welk.capitalize()
                t = (''.join((t0,t1,t2)))
        self.lines.append(t)

    def scherm_menu(self):
        with open(os.path.join(common.htmlpad, "menu.html")) as f:
            for y in f:
                y = y.rstrip()
                if "Home" in y:
                    pass
                elif "Top" in y and self.soort != "item":
                    continue # y = ''
                elif "Nieuw" in y:
                    if self.wat == "start":
                        if self.proj == "0":
                            y = y.replace("%wat","project")
                            y = y.replace("%s","Nieuw project")
                        else:
                            continue # y = y.replace("%s","Nieuwe %wat%cat")
                    else:
                        if self.welk == "nieuw" or \
                                (self.welk == "" and self.soort != "list"):
                            continue # y = ''
                        else:
                            y = y.replace("%s","Nieuwe %wat%cat")
                elif "Vorige" in y:
                    if not self.wijzig and self.soort == "item" \
                            and self.welk != "nieuw" and self.vorige != "":
                        y = y.replace("%vorige", self.vorige)
                    else:
                        continue # y = ''
                elif "Volgende" in y:
                    if not self.wijzig and self.soort == "item" \
                            and self.welk != "nieuw" and self.volgende != "":
                        y = y.replace("%volgende", self.volgende)
                    else:
                        continue # y = ''
                elif "Wijzig" in y:
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
                elif "Bekijk" in y:
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
                elif (self.wat == "start" or self.cat == "wijz") \
                        and self.proj == "0" and "<li><a" in y:
                    continue # y = ''
                y = y.replace("%cgipad",common.cgipad)
                y = y.replace("%wat",self.wat)
                y = y.replace("%proj",self.proj)
                y = y.replace("%cat",self.cat)
                y = y.replace("%welk",self.welk)
                if y != '':
                    self.lines.append(y)

    def scherm_content(self):
        "inhoud samenstellen van het menu- of gegevensgedeelte"
        self.lines.append('<span style="width: 100%; height: 600px; overflow: auto">')
        if self.soort == "item" and self.welk != "nieuw" and not self.wijzig:
            di = ItemList("project")
            p = di.items[int(self.proj)]
            self.lines.append('<span class="headr">Hoort bij project: '
                '<a href="%sshow.py?type=list&amp;what=start&amp;proj=%s">%s'
                '</a></span><br/>' % (common.cgipad, p[0], p[1]))
        if self.htmlofxml == "html": # start, nieuw of item in wijzigstand: contents begint/eindigt met html stuk
            self.printh = PrintHTMLObject(self)
            for x in self.printh.lines:
                self.lines.append(x)
        else: # self.soort == "item" and self.welk != "nieuw":
            self.printh = PrintXMLObject(self)
            for y in self.printh.regels:
                self.lines.append(y)
        # if self.wat == "start" and self.proj == "0":
        #     # used to be a warning about the dropdown menu possibly not working in IE
        #     with open(os.path.join(common.htmlpad, "browser.html")) as f:
        #         self.lines.extend([x for x in f])
        self.lines.append('</span>')
