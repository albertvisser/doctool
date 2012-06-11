import os
import common
import docobj
from relaties import Relaties
from docitems import ItemList, laatste_wijz

def selector(proj, marge=True, size=0, form=True):
    s_proj = str(proj)
    r = []
    if form:
        r.append('  <form action="%sshow.py" method="post">' % common.cgipad)
    if marge:
        h = ""
        if size > 1:
            h = "Selecteer een project:"
        r.append('    <span class="kw1 aright">%s&nbsp;</span>' % h)
        r.append('    <span class="kw3">&nbsp;')
    h = ''
    if size:
        h = (' size="%s"' % size)
        if size > 1:
            h = h + ' onclick="selectproj()"'
    else:
        h = ' onchange="form.submit()"'
    r.append('    <select name="proj" id="proj"%s>' % h)
    h = '      <option %s value="%s">%s</option>'
    rd = h.split("%s")
    i = ItemList("project")
    #~ i.read() #- zit al in __init__
    for x in i.items:
        if x[0] == "0":
            continue
        sl = ""
        if x[0] == s_proj:
            sl = 'selected="selected"'
        r.append('%s%s%s%s%s%s - %s%s' % (rd[0],sl,rd[1],x[0],rd[2],x[1],x[2],rd[3]))
    r.append('    </select>')
    if form:
        r.append('    <input type="hidden" id="type" name="type" value="list" />')
        r.append('    <input type="hidden" id="what" name="what" value="start" />')
    h = '<br /><span class="indent1">(kies eventueel een ander project)</span>'
    if size:
        h = ""
    r.append('    &nbsp;&nbsp;%s' % h)
    if marge:
        r.append('  </span>')
    if size > 1:
        r.append('    <span class="kw1 aright">en&nbsp;</span>')
        r.append('    <span class="kw3">')
        r.append('      &nbsp;&nbsp;<input type="submit" id = "subThis" disabled="disabled" value="ga naar de homepage"/>&nbsp;ervan')
        r.append('    </span>')
    if form:
        r.append('  </form>')
    return r

class PrintHTMLObject:
    "gebruikt bij start, nieuw of wijzigstand"
    def __init__(self,caller):
        self.soort = caller.soort
        self.wat = caller.wat
        self.cat = caller.cat
        self.welk = caller.welk
        self.proj = caller.proj
        fh = open(caller.fnaam)
        regels = fh.readlines()
        fh.close()
        # beginnen met een selector of een xmlobject te printen
        if self.wat == "start":
            if self.proj == "0":
                self.lines = selector(0,True,10)
            else:
                self.lines = selector(self.proj)
                self.printh = docobj.Project(self.proj)
                self.printh.read()
        elif self.welk == "nieuw":
            self.lines = [] # geen selector(self.proj)
        else:
            printh = PrintXMLObject(caller)
            self.lines = []
        overslaan = True
        for y in regels:
            h = y.rstrip()
            if overslaan:
                if "<body>" in h:
                    overslaan = False
            elif "</body>" in h:
                overslaan = True
            elif "%s" in h:
                if self.wat == "start":
                    self.verwerk_start(h)
                elif self.welk == "nieuw":
                    self.verwerk_nieuw(h)
                else:
                    rd = h.split("%s")
                    r = printh.bouwregel(rd[0])
                    if len(r) == 1:
                        s = r[0]
                    else:
                        s = "\n".join(r)
                    self.lines.append(h % s)
            else:
                self.lines.append(h)

    def verwerk_start(self,h):
        "%s regels voor een start scherm"
        if h.find("stylesheet") > -1:
            self.lines.append(h % common.stylepad)
        elif self.proj == "0":
            z = "user"
            y = "wijz"
            c = z + "_" + y
            #~ self.lines.append('  <span class="indent1">')
            try:
                self.lines.append(h % (common.cgipad, z, "0", y,
                    common.titel_menu[c]))
            except:
                self.lines.append(h % common.cgipad)
        else:
            if h.find("Naam") > -1:
                ## self.lines.append(h % self.printh.naam) # staat al in de selector
                pass
            elif h.find("Kort") > -1:
                self.lines.append(h % self.printh.kort)
            elif h.find("Oms") > -1:
                #~ self.lines.append(h % "".join(self.printh.Oms))
                self.lines.append(h % self.printh.oms)
            elif h.find("start") > -1:
                self.lines.append(h % self.printh.start)
            elif h.find("Fysiek") > -1:
                self.lines.append(h % self.printh.fysloc)
            elif h.find("Voortgang") > -1:
                #~ self.lines.append(h % "".join(self.printh.Status))
                self.lines.append(h % self.printh.status)

    def verwerk_nieuw(self,h):
        rd = h.split("%s")
        s = ''
        if h.find("hProj") >= 0:
            if self.wat != "user" or self.cat != "wijz": # bij userwijz met proj 0 moet deze via selector komen
                s = self.proj
        elif h.find("hCat") >= 0:
            s = self.cat
        elif h.find("hWat") >= 0:
            s = self.wat
        elif h.find("hType") >= 0:
            s = self.soort
        elif h.find("hName") >= 0:
            s = self.welk
        elif h.find("nieuwe document") >= 0:
            if self.wat == "user" and self.cat == "wijz":
                s = 'een titel en kies een project'
            else:
                s = 'een naam en een titel op'
        elif h.find("txtNaam") >= 0:
            if self.wat == "user" and self.cat == "wijz":
                num, nieuwetitel = laatste_wijz()
                deel1, deel2, deel3 = h.split("><")
                s = deel2.replace("text","hidden") % nieuwetitel
                self.lines.append("%s>%s<%s><%s" % (deel1.replace("nw2",
                    "nw2 vmid"), nieuwetitel, s, deel3))
            else:
                self.lines.append(h % s)
            s = ''
        elif "project" in h and self.wat == "user" and self.cat == "wijz":
            if self.proj == "0":
                s = '\n'.join(selector(0, marge=False, size=1, form=False))
            else:
                p = docobj.Project(self.proj)
                p.read()
                s = str(p) # p.naam + " - " + p.kort
        if s != '':
            self.lines.append(s.join(rd))

class PrintXMLObject:
    def __init__(self,caller):
        self.soort = caller.soort
        self.wat = caller.wat
        self.cat = caller.cat
        self.welk = caller.welk
        self.proj = caller.proj
        self.zoek = caller.zoek
        self.ok = True
        if self.soort == "item":
            self.leesitem()
            self.regels = self.toonitem() # eigenlijk hoeft deze niet als caller.edit = True
        else:
            self.regels = self.leeslist()

    def leesitem(self): # versie 2: opgenomen in itemlist.py
        if self.wat == 'project':
            self.dh = docobj.Project(self.proj)
        elif self.zoek == 'user_spec':
            self.dh = docobj.Userspec(self.welk)
        elif self.zoek == 'user_docs':
            self.dh = docobj.UserDoc(self.welk)
        elif self.zoek == 'user_wijz':
            self.dh = docobj.Userwijz(self.welk)
        elif self.zoek == 'func_docs':
            self.dh = docobj.FuncDoc(self.welk)
        elif self.zoek == 'func_task':
            self.dh = docobj.Functask(self.welk)
        elif self.zoek == 'func_proc':
            self.dh = docobj.Funcproc(self.welk)
        elif self.zoek == 'func_data':
            self.dh = docobj.Entiteit(self.welk)
        elif self.zoek == 'tech_proc':
            self.dh = docobj.Techproc(self.welk)
        elif self.zoek == 'tech_task':
            self.dh = docobj.Techtask(self.welk)
        elif self.zoek == 'tech_data':
            self.dh = docobj.Techdata(self.welk)
        elif self.zoek == 'proc_proc':
            self.dh = docobj.Procproc(self.welk)
        else:
            self.ok = False
        if self.ok:
            self.dh.read()
            if self.wat != 'project':
                self.rh = Relaties(self.wat + self.cat, self.welk)
                if self.rh.exists:
                    self.rh.read()

    def leeslist(self):
        marge = False
        lijst = selector(self.proj,marge)
        zoek = self.wat + self.cat
        di = ItemList("project")
        #~ di.read() #- zit al in __init__
        dh = ItemList(zoek, self.proj)
        if dh.exists:
            #~ dh.read() #- zit al in __init__
            pad = common.cgipad + "show.py"
            if dh.aant_items > 0:
                for x in range(dh.aant_items):
                    y = dh.items[x]
                    if self.proj == "0":
                        z = di.items[int(y[0])]
                        lijst.append('   <a target="_top" href="%s?type=item&amp;'
                            'what=%s&amp;proj=%s&amp;cat=%s&amp;which=%s">%s: %s ('
                            '%s)</a><br />' % (pad, self.wat, y[0], self.cat, y[1],
                            y[1], y[2], z[1]))
                    else:
                        lijst.append('   <a target="_top" href="%s?type=item&amp;'
                            'what=%s&amp;proj=%s&amp;cat=%s&amp;which=%s">%s: %s'
                            '</a><br />' % (pad, self.wat, self.proj, self.cat,
                            y[0], y[0], y[1]))
            else:
                lijst.append('Nog geen %s%ss gevonden voor dit project' % (self.wat,
                    self.cat))
        else:
            lijst.append('Geen Itemlist gevonden voor %s%s bij project %s<br />' % (
                self.wat, self.cat, self.proj))
        return lijst

    def toonitem(self):
        self.rgl = []
        if  self.wat == "list":
            self.rgl= selector(self.proj)
        s = self.maak_html(self.dh)
        for x in s:
            if self.zoek == 'func_data':
                if x.startswith('<-- sleutel verwijst naar '):
                    xx = x[:27]
                    xy = x[28:-1]
                    self.rgl.append('%s<a href="%sshow.py?type=item&amp;what=func'
                        '&amp;proj=%s&amp;cat=data&amp;which=%s">%s</a>' % (xx,
                        cgipad, self.proj, xy, xy))
                else:
                    self.rgl.append(x)
            else:
                self.rgl.append(x)
        if self.wat == "project":
            s = []
        else:
            s = self.maak_html(self.rh)
        for x in s:
            self.rgl.append(x)
        self.rgl.append('<br/>')
        if self.zoek == "user_spec":
            self.add_knop("pbNewFD","Opvoeren algemeen document","func","docs")
        elif self.zoek == "user_docs":
            pass
        elif self.zoek == "user_wijz":
            pass
        elif self.zoek == "func_docs":
            self.add_knop("pbNewFT","Opvoeren gebruikerstaak","func","task")
            self.add_knop("pbNewFP","Opvoeren functioneel proces","func","proc")
        elif self.zoek == "func_task":
            self.add_knop("pbNewFP","Opvoeren functioneel proces","func","proc")
            self.add_knop("pbNewTT","Opvoeren job/transactie","tech","task")
        elif self.zoek == "func_proc":
            self.add_knop("pbNewFP","Opvoeren functioneel (sub)proces","func","proc")
            self.add_knop("pbNewFD","Opvoeren funct. databeschrijving","func","data")
            self.add_knop("pbNewTP","Opvoeren technisch proces","tech","proc")
        elif self.zoek == "func_data":
            self.add_knop("pbNewTD","Opvoeren techn. databeschrijving","tech","data")
        elif self.zoek == "tech_task":
            self.add_knop("pbNewTP","Opvoeren technisch proces","tech","proc")
        elif self.zoek == "tech_proc":
            self.add_knop("pbNewTP","Opvoeren technisch (sub)proces","tech","proc")
            self.add_knop("pbNewTD","Opvoeren techn. databeschrijving","tech","data")
            self.add_knop("pbNewPP","Opvoeren programmabeschrijving","proc","proc")
        elif self.zoek == "tech_data":
            pass
        elif self.zoek == "proc_proc":
            pass
        return self.rgl

    def add_knop(self, h1, h2, h3, h4):
        zoek = "".join(self.zoek.split("_"))
        knop = '<input type="button" name="%s" id="%s" value="%s" onclick="%s" />'
        h5 = ("javascript:document.location='%sshow.py?type=item&amp;which=%s&amp;"
            "cat=%s&amp;what=nieuw&amp;vtype=%s&amp;vnaam=%s'\n" % (common.cgipad,
            h3, h4, zoek, self.wat))
        self.rgl.append(knop % (h1, h1, h2, h5))

    def maak_html(self, obj):
        s = []
        # bepaal om te beginnen het type van het object
        h = obj.__class__.__name__
        if h == "Project":
            s.append('<br /><div><span class="headr">Naam Project:</span> %s</div>'
                % obj.naam)
            s.append('<hr /><div class="headr">Omschrijving: </div><p>%s</p>'
                % obj.kort)
            s.append('<br /><div><span class="headr">Opstarten met:</span> %s</div>'
                % obj.start)
            s.append('<br /><div><span class="headr">Fysieke locatie</span> %s</div>'
                % obj.fysloc)
            s.append('<hr /><div class="headr">Opmerkingen: </div><p>%s</p>'
                % obj.status)
        elif h == "Userspec":
            s.append('<br /><div><span class="headr">Korte omschrijving:</span> %s'
                '</div>' % obj.kort)
            if len(obj.functie) > 0:
                s.append('<hr /><div class="headr">Gewenste functionaliteit: </div>')
                for x in obj.functie:
                    s.append('<p>%s</p>' % x)
            if len(obj.beeld) > 0:
                s.append('<hr /><div class="headr">Gewenste vormgeving: </div>')
                for x in obj.beeld:
                    s.append('<p>%s</p>' % x)
            if len(obj.product) > 0:
                s.append('<hr /><div class="headr">Gewenst(e) uitvoerproduct(en): </div>')
                for x in obj.product:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Randvoorwaarden: </div>')
            s.append('<div><span class="underline">Wat moet het opleveren:'
                '</span>&nbsp;%s</div>' % obj.kosten)
            s.append('<div><span class="underline">Wat mag het kosten:</span>'
                '&nbsp;%s</div>' % obj.baten)
            if len(obj.omgeving) > 0:
                for x in obj.omgeving:
                    s.append('<p>%s</p>' % x)
        elif h == "UserDoc":
            s.append('<br /><div><span class="headr">Zie:</span> %s</div>' % obj.link)
            s.append('<p>')
            if len(obj.tekst) > 0:
                for x in obj.tekst:
                    s.append('%s<br/>' % x)
            s.append('</p>')
        elif h == "Userwijz":
            s.append('<br /><div><span class="headr">Wens:</span> %s</div>' % obj.wens)
            s.append('<hr /><div class="headr">Oplossing: </div>')
            if len(obj.oplossing) > 0:
                for x in obj.oplossing:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Functionele aspecten: </div>')
            if len(obj.funcaanv) > 0:
                for x in obj.funcaanv:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Technische aspecten: </div>')
            if len(obj.techaanv) > 0:
                for x in obj.techaanv:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Realisatie aspecten: </div>')
            if len(obj.realisatie) > 0:
                for x in obj.realisatie:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Opmerkingen: </div>')
            if len(obj.opmerkingen) > 0:
                for x in obj.opmerkingen:
                    s.append('<p>%s</p>' % x)
        elif h == "FuncDoc":
            s.append('<p>')
            if len(obj.tekst) > 0:
                for x in obj.tekst:
                    s.append('%s<br/>' % x)
            s.append('</p>')
        elif h == "Funcproc":
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % obj.doel)
            s.append('<hr /><div class="headr">Wanneer/hoe vaak uitvoeren: </div>')
            if len(obj.wanneer) > 0:
                for x in obj.wanneer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Wie mag/moet dit uitvoeren: </div>')
            if len(obj.wie) > 0:
                for x in obj.wie:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Waarvoor dient het uitvoeren: </div>')
            if len(obj.waarvoor) > 0:
                for x in obj.waarvoor:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Uitgangssituatie: </div>')
            if len(obj.invoer) > 0:
                for x in obj.invoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Onder welke condities: </div>')
            if len(obj.condities) > 0:
                for x in obj.condities:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Resultaatsituatie: </div>')
            if len(obj.uitvoer) > 0:
                for x in obj.uitvoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Beschrijving: </div>')
            if len(obj.beschrijving) > 0:
                for x in obj.beschrijving:
                    s.append('<p>%s</p>' % x)
        elif h == "Functask":
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % obj.doel)
            s.append('<hr /><div class="headr">Wanneer/hoe vaak uitvoeren: </div>')
            if len(obj.wanneer) > 0:
                for x in obj.wanneer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Wie mag/moet dit uitvoeren: </div>')
            if len(obj.wie) > 0:
                for x in obj.wie:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Waarvoor dient het uitvoeren: </div>')
            if len(obj.waarvoor) > 0:
                for x in obj.waarvoor:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Onder welke condities: </div>')
            if len(obj.condities) > 0:
                for x in obj.condities:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Beschrijving: </div>')
            if len(obj.beschrijving) > 0:
                for x in obj.beschrijving:
                    s.append('<p>%s</p>' % x)
        elif h == "Entiteit":
            s.append('<br /><div><span class="headr">Entiteit naam:</span> %s</div>' % obj.naam)
            s.append('<hr /><div><span class="headr">Functie:</span> %s</div>' % obj.functie)
            s.append('<hr /><div class="headr">Attributen: </div>')
            s.append('<div class="indt">')
            if len(obj.attribuut) > 0:
                for x in obj.attribuut:
                    h = ""
                    for y in obj.toegang.keys():
                        if y == x[0]:
                            h = ("<-- identificerende sleutel (%s)" % obj.toegang[y])
                            break
                    if h == "":
                        for y in obj.relatie.keys():
                            if y == x[0]:
                                h = ('<-- sleutel verwijst naar (%s)' % obj.relatie[y])
                                break
                    s.append('<span class="underline">naam:</span> %s %s<br />' % (x[0],h))
                    s.append('<span class="underline">type:</span> %s<br />' % x[1])
                    s.append('<span class="underline">omschrijving:</span> %s<br />' % x[2])
                    s.append('<span class="underline">bijzonderheden:</span> %s<br />' % x[3])
                    s.append('<br />')
            s.append('</div>' )
            s.append('<hr /><div class="headr">Levenscyclus: </div>')
            if len(obj.levensloop) > 0:
                for x in obj.levensloop:
                    s.append('<p>%s</p>' % x)
        elif h == "Techproc":
            s.append('<br /><div><span class="headr">Titel:</span> %s</div>' % obj.titel)
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % obj.doel)
            s.append('<hr /><div class="headr">Uitgangssituatie: </div>')
            if len(obj.invoer) > 0:
                for x in obj.invoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Resultaatsituatie: </div>')
            if len(obj.uitvoer) > 0:
                for x in obj.uitvoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Beschrijving: </div>')
            if len(obj.beschrijving) > 0:
                for x in obj.beschrijving:
                    s.append('<p>%s</p>' % x)
        elif h == "Techtask":
            s.append('<br /><div><span class="headr">Korte beschrijving:</span> %s'
                '</div>' % obj.kort)
            s.append('<br /><div class="headr">Doel: </div>')
            if len(obj.doel) > 0:
                for x in obj.doel:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Periodiciteit: </div>')
            if len(obj.periode) > 0:
                for x in obj.periode:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Verloop: </div>')
            if len(obj.verloop) > 0:
                for x in obj.verloop:
                    s.append('<p>%s</p>' % x)
        elif h == "Record": #Techdata
            pass
        elif h == "Procproc":
            s.append('<br /><div><span class="headr">Titel:</span> %s</div>' % obj.titel)
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % obj.doel)
            s.append('<hr /><div class="headr">Invoersituatie (obj.a. argumenten bij aanroep): </div>')
            if len(obj.invoer) > 0:
                for x in obj.invoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Uitvoersituatie (incl. foutmeldingen): </div>')
            if len(obj.uitvoer) > 0:
                for x in obj.uitvoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Werkwijze: </div>')
            if len(obj.werkwijze) > 0:
                for x in obj.werkwijze:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Bijzonderheden: </div>')
            if len(obj.bijzonder) > 0:
                for x in obj.bijzonder:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Hoetetesten: </div>')
            if len(obj.hoetetesten) > 0:
                for x in obj.hoetetesten:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Testgevallen: </div>')
            if len(obj.testgevallen) > 0:
                for x in obj.testgevallen:
                    s.append('<p>%s</p>' % x)
        elif h == "Relaties":
            hr = ('<a href="%sshow.py?type=item&amp;what=$$&amp;proj=%s&amp;'
                'cat=$$&amp;which=$$">$$</a>' % (common.cgipad,self.proj))
            href = hr.replace("$$","%s")
            for x in obj.relnaar.keys():
                if x == "userspec":
                    t = "Hoort bij gebruikersspecificatie"
                elif x == "functask":
                    t = "wordt gebruikt door gebruikerstaak"
                elif x == "funcproc":
                    t = "wordt gebruikt door functioneel proces"
                elif x == "funcdata":
                    t = "Naar Funcdata"
                elif x == "techtask":
                    t = "hoort bij technische taak (job/transactie)"
                elif x == "techproc":
                    t = "hoort bij technisch(e) proces(sen)"
                elif x == "techdata":
                    t = "Naar Techdata"
                elif x == "procproc":
                    t = "Naar Procproc"
                s.append('<span class="headr">%s: </span>' % t)
                h = ""
                for y in obj.relnaar[x]:
                    s.append(h)
                    if h == "": h = ", "
                    s.append(href % (x[:4],x[4:],y,y))
                s.append('<br />')
            for x in obj.relvan.keys():
                if x == "userspec":
                    t = "Bijbehorende gebruikersspecificatie(s)"
                elif x == "functask":
                    t = "Bijbehorende gebruikersta(a)k(en)"
                elif x == "funcproc":
                    t = "Bijbehorende functione(e)le proces(sen)"
                elif x == "funcdata":
                    t = "Van Funcdata"
                elif x == "techtask":
                    t = "Bijbehorende technische ta(a)k(en) (job/transactie)"
                elif x == "techproc":
                    t = "Bijbehorend(e) technisch(e) proces(sen)"
                elif x == "techdata":
                    t = "wordt technisch verder gespecificeerd in"
                elif x == "procproc":
                    t = "Bijbehorende realisatie/procedurebeschrijving(en)"
                s.append('<span class="headr">%s: </span>' % t)
                h = ""
                for y in obj.relvan[x]:
                    s.append(h)
                    if h == "": h = ", "
                    s.append(href % (x[:4],x[4:],y,y))
                s.append('<br />')
        return s

    def bouwregel(self,regeldeel):
        # moet deze eigenlijk ook niet per object(type) in plaats van per veldnaam?
        rd = regeldeel.split() # eerste stuk opdelen in woorden
        sel = ""
        for x in rd:
            if x[0:3] == "id=":
                sel = x[4:-1]
                break
        rgl = []
        if sel == "hWhat":
            rgl.append(self.wat)
            #~ rgl.append(self.zoek[:4])
        elif sel == "hCat":
            rgl.append(self.cat)
            #~ categorie = self.zoek[4:]
            #~ rgl.append(categorie)
        elif sel == "hProj":
            rgl.append(self.proj)
        elif sel == "hWhich":
            rgl.append(self.welk)
        # bij txt... nog toevoegen:
        #   techdata gegevens (functie,opbouw,toegang,relatie,levensloop)>
        elif sel == "txtAttr":
            self.h = ""
            if len(self.dh.attribuut) > 0:
                for x in self.dh.attribuut:
                    for y in self.dh.toegang.keys():
                        if y == x[0]:
                            hself.h = ("deze (%s)" % self.dh.toegang[y])
                            break
                    for y in self.dh.relatie.keys():
                        if y == x[0]:
                            hself.h = ('%s' % self.dh.relatie[y])
                            break
                    rgl.append('naam: %s (%s), sleutel voor %s\noms:  %s\nbijz: %s\n\n' % (x[0],x[1],hh,x[2],x[3]))
        elif sel == "txtBaten":
            rgl.append(self.dh.baten)
        elif sel == "txtBeeld":
            if len(self.dh.beeld) > 0:
                for x in self.dh.beeld:
                    rgl.append(x)
        elif sel == "txtBeschr":
            if len(self.dh.beschrijving) > 0:
                for x in self.dh.beschrijving:
                    rgl.append(x)
        elif sel == "txtBijzonder":
            if len(self.dh.bijzonder) > 0:
                for x in self.dh.bijzonder:
                    rgl.append(x)
        elif sel == "txtCond":
            if len(self.dh.condities) > 0:
                for x in self.dh.condities:
                    rgl.append(x)
        elif sel == "txtDoel":
            if self.zoek == "techtask":
                if len(self.dh.doel) > 0:
                    for x in self.dh.doel:
                        rgl.append(x)
            else:
                rgl.append(self.dh.doel)
        elif sel == "txtFunc":
            if len(self.dh.functie) > 0:
                for x in self.dh.functie:
                    rgl.append(x)
        elif sel == "txtFuncA":
            if len(self.dh.funcaanv) > 0:
                for x in self.dh.funcaanv:
                    rgl.append(x)
        elif sel == "txtFunctie":
            rgl.append(self.dh.functie)
        elif sel == "txtFysloc":
            rgl.append(self.dh.fysloc)
        elif sel == "txtHoeTesten":
            if len(self.dh.hoetetesten) > 0:
                for x in self.dh.hoetetesten:
                    rgl.append(x)
        elif sel == "txtInvoer":
            if len(self.dh.invoer) > 0:
                for x in self.dh.invoer:
                    rgl.append(x)
        elif sel == "txtKort":
            rgl.append(self.dh.kort)
        elif sel == "txtKosten":
            rgl.append(self.dh.kosten)
        elif sel == "txtLifeC":
            if len(self.dh.levensloop) > 0:
                for x in self.dh.levensloop:
                    rgl.append(x)
        elif sel == "txtLink":
            rgl.append(self.dh.link)
        elif sel == "txtNaam":
            rgl.append(self.dh.naam)
        elif sel == "txtNummer":
            rgl.append(self.dh.nummer)
        elif sel == "txtOmg":
            if len(self.dh.omgeving) > 0:
                for x in self.dh.omgeving:
                    rgl.append(x)
        elif sel == "txtOms":
            #~ if len(self.dh.Oms) > 0:
                #~ for x in self.dh.Oms:
                    #~ rgl.append(x)
            rgl.append(self.dh.oms)
        elif sel == "txtOplos":
            if len(self.dh.oplossing) > 0:
                for x in self.dh.oplossing:
                    rgl.append(x)
        elif sel == "txtOpm":
            #~ if len(self.dh.Status) > 0:
                #~ for x in self.dh.Status:
                    #~ rgl.append(x)
            rgl.append(self.dh.status)
        elif sel == "txtOpmerking":
            if len(self.dh.opmerkingen) > 0:
                for x in self.dh.opmerkingen:
                    rgl.append(x)
        elif sel == "txtPeriode":
            if len(self.dh.periode) > 0:
                for x in self.dh.periode:
                    rgl.append(x)
        elif sel == "txtProduct":
            if len(self.dh.product) > 0:
                for x in self.dh.product:
                    rgl.append(x)
        elif sel == "txtRealA":
            if len(self.dh.realisatie) > 0:
                for x in self.dh.realisatie:
                    rgl.append(x)
        elif sel == "txtStart":
            rgl.append(self.dh.start)
        elif sel == "txtTechA":
            if len(self.dh.techaanv) > 0:
                for x in self.dh.techaanv:
                    rgl.append(x)
        elif sel == "txtTestset":
            if len(self.dh.Testgevallen) > 0:
                for x in self.dh.testgevallen:
                    rgl.append(x)
        elif sel == "txtTekst":
            if len(self.dh.tekst) > 0:
                for x in self.dh.tekst:
                    rgl.append(x)
        elif sel == "txtTitel":
            rgl.append(self.dh.titel)
        elif sel == "txtUitvoer":
            if len(self.dh.uitvoer) > 0:
                for x in self.dh.uitvoer:
                    rgl.append(x)
        elif sel == "txtVerloop":
            if len(self.dh.verloop) > 0:
                for x in self.dh.verloop:
                    rgl.append(x)
        elif sel == "txtWaarvoor":
            if len(self.dh.waarvoor) > 0:
                for x in self.dh.waarvoor:
                    rgl.append(x)
        elif sel == "txtWanneer":
            if len(self.dh.wanneer) > 0:
                for x in self.dh.wanneer:
                    rgl.append(x)
        elif sel == "txtWens":
            rgl.append(self.dh.wens)
        elif sel == "txtWie":
            if len(self.dh.wie) > 0:
                for x in self.dh.wie:
                    rgl.append(x)
        else:
            hl1 = ["selUserspec", "selUserwijz", "selFunctask", "selFuncproc",
                "selFuncdata", "selTechtask", "selTechproc", "selTechdata",
                "selProcproc"]
            hl2 = ["userspec", "userwijz", "functask", "funcproc", "funcdata",
                "techtask", "techproc", "techdata", "procproc"]
            for idx, item in enumerate(hl1):
                if item == sel:
                    #~ self.h = "\n"
                    lh = ItemList(hl2[idx]) # was lself.h = ItemList(hl2[i])
                    #~ lh.read() # -  zit al in __init__
                    for item in lh.items:
                        sel_text = ""
                        if idx == 0:
                            zk = self.rh.relnaar['userspec']
                        elif idx == 1:
                            zk = self.rh.relnaar['userwijz']
                        elif idx == 2:
                            zk = self.rh.relnaar['functask']
                        elif idx == 3:
                            zk = self.rh.relnaar['funcproc']
                        elif idx == 4:
                            zk = self.rh.relnaar['funcdata']
                        elif idx == 5:
                            zk = self.rh.relnaar['techtask']
                        elif idx == 6:
                            zk = self.rh.relnaar['techproc']
                        #~ elif idx == 7:
                            #~ zk = self.rh.VTechdata
                        elif idx == 8:
                            zk = self.rh.relnaar['procproc']
                        for y in zk:
                            if y == item:
                                sel_text = " selected"
                                break
                        hs = ('      <option%s value="%s">%s: %s</option>' % (
                            sel_text, item[0], item[0], item[1]))
                        rgl.append(hs)
                    rgl.append("    ")
                    break
        return rgl
