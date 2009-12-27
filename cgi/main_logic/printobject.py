from doctool_globals import *
from os.path import exists

def selector(proj,marge=True,size=0,form=True):
    s_proj = str(proj)
    r = []
    if form:
        r.append('  <form action="%sshow.py" method="post">' % cgipad)
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
    from docitems import ItemList
    i = ItemList("project")
    #~ i.read() #- zit al in __init__
    for x in i.Items:
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

class printHTMLObject:
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
                from project import Project
                self.printh = Project(self.proj)
                self.printh.read()
        elif self.welk == "nieuw":
            self.lines = [] # geen selector(self.proj)
        else:
            printh = printXMLObject(caller)
            self.lines = []
        overslaan = True
        for y in regels:
            h = y[:-1]
            if overslaan:
                if h == "<body>": overslaan = False
            elif h == "</body>":
                overslaan = True
            elif h.find("%s") >= 0:
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
                    self.lines.append("%s%s%s"% (rd[0], s, rd[1]))
            else:
                self.lines.append(h)

    def verwerk_start(self,h):
        "%s regels voor een start scherm"
        if h.find("stylesheet") > -1:
            self.lines.append(h % stylepad)
        elif self.proj == "0":
            z = "user"
            y = "wijz"
            c = z + "_" + y
            #~ self.lines.append('  <span class="indent1">')
            try:
                self.lines.append(h % (cgipad,z,"0",y,titel_menu[c]))
            except:
                self.lines.append(h % cgipad)
        else:
            if h.find("Naam") > -1:
                self.lines.append(h % self.printh.Naam)
            elif h.find("Kort") > -1:
                self.lines.append(h % self.printh.Kort)
            elif h.find("Oms") > -1:
                #~ self.lines.append(h % "".join(self.printh.Oms))
                self.lines.append(h % self.printh.Oms)
            elif h.find("start") > -1:
                self.lines.append(h % self.printh.Start)
            elif h.find("Fysiek") > -1:
                self.lines.append(h % self.printh.Fysloc)
            elif h.find("Voortgang") > -1:
                #~ self.lines.append(h % "".join(self.printh.Status))
                self.lines.append(h % self.printh.Status)

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
                from docitems import LaatsteWijz
                dh = LaatsteWijz()
                hh = h.split("><")
                s = (hh[1].replace("text","hidden") % dh.nieuwetitel)
                self.lines.append("%s>%s<%s><%s" % (hh[0].replace("nw2","nw2 vmid"),dh.nieuwetitel,s,hh[2]))
            else:
                self.lines.append(h % s)
            s = ''
        elif h.find("project") >= 0 and self.wat == "user" and self.cat == "wijz":
            if self.proj == "0":
                s = '\n'.join(selector(0,marge=False,size=1,form=False))
            else:
                from project import Project
                p = Project(self.proj)
                p.read()
                s = p.Naam + " - " + p.Kort
        if s != '':
            self.lines.append(s.join(rd))

class printXMLObject:
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
            from project import Project
            self.dh = Project(self.proj)
        elif self.zoek == 'user_spec':
            from userspec import Userspec
            self.dh = Userspec(self.welk)
        elif self.zoek == 'user_docs':
            from userdocs import UserDoc
            self.dh = UserDoc(self.welk)
        elif self.zoek == 'user_wijz':
            from userwijz import Userwijz
            self.dh = Userwijz(self.welk)
        elif self.zoek == 'func_docs':
            from funcdocs import FuncDoc
            self.dh = FuncDoc(self.welk)
        elif self.zoek == 'func_task':
            from functask import Functask
            self.dh = Functask(self.welk)
        elif self.zoek == 'func_proc':
            from funcproc import Funcproc
            self.dh = Funcproc(self.welk)
        elif self.zoek == 'func_data':
            from funcdata import Entiteit
            self.dh = Entiteit(self.welk)
        elif self.zoek == 'tech_proc':
            from techproc import Techproc
            self.dh = Techproc(self.welk)
        elif self.zoek == 'tech_task':
            from techtask import Techtask
            self.dh = Techtask(self.welk)
        elif self.zoek == 'tech_data':
            from techdata import Techdata
            self.dh = Techdata(self.welk)
        elif self.zoek == 'proc_proc':
            from procproc import Procproc
            self.dh = Procproc(self.welk)
        else:
            self.ok = False
        if self.ok:
            self.dh.read()
            if self.wat != 'project':
                from relaties import Relaties
                self.rh = Relaties(self.wat + self.cat,self.welk)
                if self.rh.exists:
                    self.rh.read()

    def leeslist(self):
        marge=False
        lijst = selector(self.proj,marge)
        zoek = self.wat + self.cat
        from docitems import ItemList
        di = ItemList("project")
        #~ di.read() #- zit al in __init__
        dh = ItemList(zoek,self.proj)
        if dh.exists:
            #~ dh.read() #- zit al in __init__
            pad = cgipad + "show.py"
            if dh.aantItems > 0:
                for x in range(dh.aantItems):
                    y = dh.Items[x]
                    if self.proj == "0":
                        z = di.Items[int(y[0])]
                        lijst.append('   <a target="_top" href="%s?type=item&amp;what=%s&amp;proj=%s&amp;cat=%s&amp;which=%s">%s: %s (%s)</a><br />'
                        % (pad,self.wat,y[0],self.cat,y[1],y[1],y[2],z[1]))
                    else:
                        lijst.append('   <a target="_top" href="%s?type=item&amp;what=%s&amp;proj=%s&amp;cat=%s&amp;which=%s">%s: %s</a><br />'
                        % (pad,self.wat,self.proj,self.cat,y[0],y[0],y[1]))
            else:
                lijst.append('Nog geen %s%ss gevonden voor dit project' % (self.wat,self.cat))
        else:
            lijst.append('Geen Itemlist gevonden voor %s%s bij project %s<br />' % (self.wat,self.cat,self.proj))
        return lijst

    def toonitem(self):
        self.rgl = []
        if  self.wat == "list":
            self.rgl= selector(self.proj)
        s = self.maakHtml(self.dh)
        for x in s:
            if self.zoek == 'func_data':
                if x[:27] == '<-- sleutel verwijst naar ':
                    xx = x[:27]
                    xy = x[28:-1]
                    self.rgl.append('%s<a href="%sshow.py?type=item&amp;what=func&amp;proj=%s&amp;cat=data&amp;which=%s">%s</a>' % (xx,cgipad,self.proj,xy,xy))
                else:
                    self.rgl.append(x)
            else:
                self.rgl.append(x)
        if self.wat == "project":
            s = []
        else:
            s = self.maakHtml(self.rh)
        for x in s:
            self.rgl.append(x)
        self.rgl.append('<br/>')
        if self.zoek == "user_spec":
            self.addKnop("pbNewFD","Opvoeren algemeen document","func","docs")
        elif self.zoek == "user_docs":
            pass
        elif self.zoek == "user_wijz":
            pass
        elif self.zoek == "func_docs":
            self.addKnop("pbNewFT","Opvoeren gebruikerstaak","func","task")
            self.addKnop("pbNewFP","Opvoeren functioneel proces","func","proc")
        elif self.zoek == "func_task":
            self.addKnop("pbNewFP","Opvoeren functioneel proces","func","proc")
            self.addKnop("pbNewTT","Opvoeren job/transactie","tech","task")
        elif self.zoek == "func_proc":
            self.addKnop("pbNewFP","Opvoeren functioneel (sub)proces","func","proc")
            self.addKnop("pbNewFD","Opvoeren funct. databeschrijving","func","data")
            self.addKnop("pbNewTP","Opvoeren technisch proces","tech","proc")
        elif self.zoek == "func_data":
            self.addKnop("pbNewTD","Opvoeren techn. databeschrijving","tech","data")
        elif self.zoek == "tech_task":
            self.addKnop("pbNewTP","Opvoeren technisch proces","tech","proc")
        elif self.zoek == "tech_proc":
            self.addKnop("pbNewTP","Opvoeren technisch (sub)proces","tech","proc")
            self.addKnop("pbNewTD","Opvoeren techn. databeschrijving","tech","data")
            self.addKnop("pbNewPP","Opvoeren programmabeschrijving","proc","proc")
        elif self.zoek == "tech_data":
            pass
        elif self.zoek == "proc_proc":
            pass
        return self.rgl

    def addKnop(self,h1,h2,h3,h4):
        zoek = "".join(self.zoek.split("_"))
        knop = '<input type="button" name="%s" id="%s" value="%s" onclick="%s" />'
        onclick = "javascript:document.location='%sshow.py?type=item&amp;which=%s&amp;cat=%s&amp;what=nieuw&amp;vtype=%s&amp;vnaam=%s'\n"
        h5 = (onclick % (cgipad,h3,h4,zoek,self.wat))
        self.rgl.append(knop % (h1,h1,h2,h5))

    def maakHtml(self,o):
        s = []
        # bepaal om te beginnen het type van het object
        h = o.__class__.__name__
        if h == "Project":
            s.append('<br /><div><span class="headr">Naam Project:</span> %s</div>' % o.Naam)
            s.append('<hr /><div class="headr">Omschrijving: </div><p>%s</p>' % o.Kort)
            s.append('<br /><div><span class="headr">Opstarten met:</span> %s</div>' % o.Start)
            s.append('<br /><div><span class="headr">Fysieke locatie</span> %s</div>' % o.Fysloc)
            s.append('<hr /><div class="headr">Opmerkingen: </div><p>%s</p>' % o.Status)
        elif h == "Userspec":
            s.append('<br /><div><span class="headr">Korte omschrijving:</span> %s</div>' % o.Kort)
            if len(o.Functie) > 0:
                s.append('<hr /><div class="headr">Gewenste functionaliteit: </div>')
                for x in o.Functie:
                    s.append('<p>%s</p>' % x)
            if len(o.Beeld) > 0:
                s.append('<hr /><div class="headr">Gewenste vormgeving: </div>')
                for x in o.Beeld:
                    s.append('<p>%s</p>' % x)
            if len(o.Product) > 0:
                s.append('<hr /><div class="headr">Gewenst(e) uitvoerproduct(en): </div>')
                for x in o.Product:
                    s.append('<p>%s</p>' % x)
            if len(o.Omgeving) > 0:
                s.append('<hr /><div class="headr">Randvoorwaarden: </div>')
                s.append('<div><span class="underline">Wat moet het opleveren:</span>&nbsp;%s</div>' % o.Omgeving[0])
                s.append('<div><span class="underline">Wat mag het kosten:</span>&nbsp;%s</div>' % o.Omgeving[1])
                for x in range(2,len(o.Omgeving)):
                    s.append('<p>%s</p>' % o.Omgeving[x])
        elif h == "UserDoc":
            s.append('<br /><div><span class="headr">Zie:</span> %s</div>' % o.Link)
            s.append('<p>')
            if len(o.Tekst) > 0:
                for x in o.Tekst:
                    s.append('%s<br/>' % x)
            s.append('</p>')
        elif h == "Userwijz":
            s.append('<br /><div><span class="headr">Wens:</span> %s</div>' % o.Wens)
            s.append('<hr /><div class="headr">Oplossing: </div>')
            if len(o.Oplossing) > 0:
                for x in o.Oplossing:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Functionele aspecten: </div>')
            if len(o.FuncAanv) > 0:
                for x in o.FuncAanv:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Technische aspecten: </div>')
            if len(o.TechAanv) > 0:
                for x in o.TechAanv:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Realisatie aspecten: </div>')
            if len(o.Realisatie) > 0:
                for x in o.Realisatie:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Opmerkingen: </div>')
            if len(o.Opmerkingen) > 0:
                for x in o.Opmerkingen:
                    s.append('<p>%s</p>' % x)
        elif h == "FuncDoc":
            s.append('<p>')
            if len(o.Tekst) > 0:
                for x in o.Tekst:
                    s.append('%s<br/>' % x)
            s.append('</p>')
        elif h == "Funcproc":
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % o.Doel)
            s.append('<hr /><div class="headr">Wanneer/hoe vaak uitvoeren: </div>')
            if len(o.Wanneer) > 0:
                for x in o.Wanneer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Wie mag/moet dit uitvoeren: </div>')
            if len(o.Wie) > 0:
                for x in o.Wie:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Waarvoor dient het uitvoeren: </div>')
            if len(o.Waarvoor) > 0:
                for x in o.Waarvoor:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Uitgangssituatie: </div>')
            if len(o.Invoer) > 0:
                for x in o.Invoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Onder welke condities: </div>')
            if len(o.Condities) > 0:
                for x in o.Condities:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Resultaatsituatie: </div>')
            if len(o.Uitvoer) > 0:
                for x in o.Uitvoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Beschrijving: </div>')
            if len(o.Beschrijving) > 0:
                for x in o.Beschrijving:
                    s.append('<p>%s</p>' % x)
        elif h == "Functask":
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % o.Doel)
            s.append('<hr /><div class="headr">Wanneer/hoe vaak uitvoeren: </div>')
            if len(o.Wanneer) > 0:
                for x in o.Wanneer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Wie mag/moet dit uitvoeren: </div>')
            if len(o.Wie) > 0:
                for x in o.Wie:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Waarvoor dient het uitvoeren: </div>')
            if len(o.Waarvoor) > 0:
                for x in o.Waarvoor:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Onder welke condities: </div>')
            if len(o.Condities) > 0:
                for x in o.Condities:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Beschrijving: </div>')
            if len(o.Beschrijving) > 0:
                for x in o.Beschrijving:
                    s.append('<p>%s</p>' % x)
        elif h == "Entiteit":
            s.append('<br /><div><span class="headr">Entiteit naam:</span> %s</div>' % o.Naam)
            s.append('<hr /><div><span class="headr">Functie:</span> %s</div>' % o.Functie)
            s.append('<hr /><div class="headr">Attributen: </div>')
            s.append('<div class="indt">')
            if len(o.Attribuut) > 0:
                for x in o.Attribuut:
                    h = ""
                    for y in o.Toegang.keys():
                        if y == x[0]:
                            h = ("<-- identificerende sleutel (%s)" % o.Toegang[y])
                            break
                    if h == "":
                        for y in o.Relatie.keys():
                            if y == x[0]:
                                h = ('<-- sleutel verwijst naar (%s)' % o.Relatie[y])
                                break
                    s.append('<span class="underline">naam:</span> %s %s<br />' % (x[0],h))
                    s.append('<span class="underline">type:</span> %s<br />' % x[1])
                    s.append('<span class="underline">omschrijving:</span> %s<br />' % x[2])
                    s.append('<span class="underline">bijzonderheden:</span> %s<br />' % x[3])
                    s.append('<br />')
            s.append('</div>' )
            s.append('<hr /><div class="headr">Levenscyclus: </div>')
            if len(o.Levensloop) > 0:
                for x in o.Levensloop:
                    s.append('<p>%s</p>' % x)
        elif h == "Techproc":
            s.append('<br /><div><span class="headr">Titel:</span> %s</div>' % o.Titel)
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % o.Doel)
            s.append('<hr /><div class="headr">Uitgangssituatie: </div>')
            if len(o.Invoer) > 0:
                for x in o.Invoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Resultaatsituatie: </div>')
            if len(o.Uitvoer) > 0:
                for x in o.Uitvoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Beschrijving: </div>')
            if len(o.Beschrijving) > 0:
                for x in o.Beschrijving:
                    s.append('<p>%s</p>' % x)
        elif h == "Techtask":
            s.append('<br /><div><span class="headr">Korte beschrijving:</span> %s</div>' % o.Kort)
            s.append('<br /><div class="headr">Doel: </div>')
            if len(o.Doel) > 0:
                for x in o.Doel:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Periodiciteit: </div>')
            if len(o.Periode) > 0:
                for x in o.Periode:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Verloop: </div>')
            if len(o.Verloop) > 0:
                for x in o.Verloop:
                    s.append('<p>%s</p>' % x)
        elif h == "Record": #Techdata
            pass
        elif h == "Procproc":
            s.append('<br /><div><span class="headr">Titel:</span> %s</div>' % o.Titel)
            s.append('<br /><div><span class="headr">Doel:</span> %s</div>' % o.Doel)
            s.append('<hr /><div class="headr">Invoersituatie (o.a. argumenten bij aanroep): </div>')
            if len(o.Invoer) > 0:
                for x in o.Invoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Uitvoersituatie (incl. foutmeldingen): </div>')
            if len(o.Uitvoer) > 0:
                for x in o.Uitvoer:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Werkwijze: </div>')
            if len(o.Werkwijze) > 0:
                for x in o.Werkwijze:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Bijzonderheden: </div>')
            if len(o.Bijzonder) > 0:
                for x in o.Bijzonder:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Hoetetesten: </div>')
            if len(o.Hoetetesten) > 0:
                for x in o.Hoetetesten:
                    s.append('<p>%s</p>' % x)
            s.append('<hr /><div class="headr">Testgevallen: </div>')
            if len(o.Testgevallen) > 0:
                for x in o.Testgevallen:
                    s.append('<p>%s</p>' % x)
        elif h == "Relaties":
            hr = ('<a href="%sshow.py?type=item&amp;what=$$&amp;proj=%s&amp;cat=$$&amp;which=$$">$$</a>' % (cgipad,self.proj))
            href = hr.replace("$$","%s")
            for x in o.relnaar.keys():
                if x == "userspec":  t = "Hoort bij gebruikersspecificatie"
                elif x == "functask":  t = "wordt gebruikt door gebruikerstaak"
                elif x == "funcproc":  t = "wordt gebruikt door functioneel proces"
                elif x == "funcdata":  t = "Naar Funcdata"
                elif x == "techtask":  t = "hoort bij technische taak (job/transactie)"
                elif x == "techproc":  t = "hoort bij technisch(e) proces(sen)"
                elif x == "techdata":  t = "Naar Techdata"
                elif x == "procproc":  t = "Naar Procproc"
                s.append('<span class="headr">%s: </span>' % t)
                h = ""
                for y in o.relnaar[x]:
                    s.append(h)
                    if h == "": h = ", "
                    s.append(href % (x[:4],x[4:],y,y))
                s.append('<br />')
            for x in o.relvan.keys():
                if x == "userspec":  t = "Bijbehorende gebruikersspecificatie(s)"
                elif x == "functask":  t = "Bijbehorende gebruikersta(a)k(en)"
                elif x == "funcproc":  t = "Bijbehorende functione(e)le proces(sen)"
                elif x == "funcdata":  t = "Van Funcdata"
                elif x == "techtask":  t = "Bijbehorende technische ta(a)k(en) (job/transactie)"
                elif x == "techproc":  t = "Bijbehorend(e) technisch(e) proces(sen)"
                elif x == "techdata":  t = "wordt technisch verder gespecificeerd in"
                elif x == "procproc":  t = "Bijbehorende realisatie/procedurebeschrijving(en)"
                s.append('<span class="headr">%s: </span>' % t)
                h = ""
                for y in o.relvan[x]:
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
            if len(self.dh.Attribuut) > 0:
                for x in self.dh.Attribuut:
                    for y in self.dh.Toegang.keys():
                        if y == x[0]:
                            hself.h = ("deze (%s)" % self.dh.Toegang[y])
                            break
                    for y in self.dh.Relatie.keys():
                        if y == x[0]:
                            hself.h = ('%s' % self.dh.Relatie[y])
                            break
                    rgl.append('naam: %s (%s), sleutel voor %s\noms:  %s\nbijz: %s\n\n' % (x[0],x[1],hh,x[2],x[3]))
        elif sel == "txtBaten":
            if len(self.dh.Omgeving) > 0:
                rgl.append(self.dh.Omgeving[0])
        elif sel == "txtBeeld":
            if len(self.dh.Beeld) > 0:
                for x in self.dh.Beeld:
                    rgl.append(x)
        elif sel == "txtBeschr":
            if len(self.dh.Beschrijving) > 0:
                for x in self.dh.Beschrijving:
                    rgl.append(x)
        elif sel == "txtBijzonder":
            if len(self.dh.Bijzonder) > 0:
                for x in self.dh.Bijzonder:
                    rgl.append(x)
        elif sel == "txtCond":
            if len(self.dh.Condities) > 0:
                for x in self.dh.Condities:
                    rgl.append(x)
        elif sel == "txtDoel":
            if self.zoek == "techtask":
                if len(self.dh.Doel) > 0:
                    for x in self.dh.Doel:
                        rgl.append(x)
            else:
                rgl.append(self.dh.Doel)
        elif sel == "txtFunc":
            if len(self.dh.Functie) > 0:
                for x in self.dh.Functie:
                    rgl.append(x)
        elif sel == "txtFuncA":
            if len(self.dh.FuncAanv) > 0:
                for x in self.dh.FuncAanv:
                    rgl.append(x)
        elif sel == "txtFunctie":
            rgl.append(self.dh.Functie)
        elif sel == "txtFysloc":
            rgl.append(self.dh.Fysloc)
        elif sel == "txtHoeTesten":
            if len(self.dh.Hoetetesten) > 0:
                for x in self.dh.Hoetesten:
                    rgl.append(x)
        elif sel == "txtInvoer":
            if len(self.dh.Invoer) > 0:
                for x in self.dh.Invoer:
                    rgl.append(x)
        elif sel == "txtKort":
            rgl.append(self.dh.Kort)
        elif sel == "txtKosten":
            if len(self.dh.Omgeving) > 0:
                rgl.append(self.dh.Omgeving[1])
        elif sel == "txtLifeC":
            if len(self.dh.Levensloop) > 0:
                for x in self.dh.Levensloop:
                    rgl.append(x)
        elif sel == "txtLink":
            rgl.append(self.dh.Link)
        elif sel == "txtNaam":
            rgl.append(self.dh.Naam)
        elif sel == "txtNummer":
            rgl.append(self.dh.Nummer)
        elif sel == "txtOmg":
            if len(self.dh.Omgeving) > 0:
                for x in range(2,len(self.dh.Omgeving)):
                    rgl.append(self.dh.Omgeving[x])
        elif sel == "txtOms":
            #~ if len(self.dh.Oms) > 0:
                #~ for x in self.dh.Oms:
                    #~ rgl.append(x)
            rgl.append(self.dh.Oms)
        elif sel == "txtOplos":
            if len(self.dh.Oplossing) > 0:
                for x in self.dh.Oplossing:
                    rgl.append(x)
        elif sel == "txtOpm":
            #~ if len(self.dh.Status) > 0:
                #~ for x in self.dh.Status:
                    #~ rgl.append(x)
            rgl.append(self.dh.Status)
        elif sel == "txtOpmerking":
            if len(self.dh.Opmerkingen) > 0:
                for x in self.dh.Opmerkingen:
                    rgl.append(x)
        elif sel == "txtPeriode":
            if len(self.dh.Periode) > 0:
                for x in self.dh.Periode:
                    rgl.append(x)
        elif sel == "txtProduct":
            if len(self.dh.Product) > 0:
                for x in self.dh.Product:
                    rgl.append(x)
        elif sel == "txtRealA":
            if len(self.dh.Realisatie) > 0:
                for x in self.dh.Realisatie:
                    rgl.append(x)
        elif sel == "txtStart":
            rgl.append(self.dh.Start)
        elif sel == "txtTechA":
            if len(self.dh.TechAanv) > 0:
                for x in self.dh.TechAanv:
                    rgl.append(x)
        elif sel == "txtTestset":
            if len(self.dh.Testgevallen) > 0:
                for x in self.dh.Testgevallen:
                    rgl.append(x)
        elif sel == "txtTekst":
            if len(self.dh.Tekst) > 0:
                for x in self.dh.Tekst:
                    rgl.append(x)
        elif sel == "txtTitel":
            rgl.append(self.dh.Titel)
        elif sel == "txtUitvoer":
            if len(self.dh.Uitvoer) > 0:
                for x in self.dh.Uitvoer:
                    rgl.append(x)
        elif sel == "txtVerloop":
            if len(self.dh.Verloop) > 0:
                for x in self.dh.Verloop:
                    rgl.append(x)
        elif sel == "txtWaarvoor":
            if len(self.dh.Waarvoor) > 0:
                for x in self.dh.Waarvoor:
                    rgl.append(x)
        elif sel == "txtWanneer":
            if len(self.dh.Wanneer) > 0:
                for x in self.dh.Wanneer:
                    rgl.append(x)
        elif sel == "txtWens":
            rgl.append(self.dh.Wens)
        elif sel == "txtWie":
            if len(self.dh.Wie) > 0:
                for x in self.dh.Wie:
                    rgl.append(x)
        else:
            hl1 = ["selUserspec","selUserwijz","selFunctask","selFuncproc","selFuncdata","selTechtask","selTechproc","selTechdata","selProcproc"]
            hl2 = ["userspec","userwijz","functask","funcproc","funcdata","techtask","techproc","techdata","procproc"]
            try:
                i = hl1.find(sel)
            except:
                selfound = False
            else:
                selfound = True
            if selfound:
                #~ self.h = "\n"
                lh = ItemList(hl2[i]) # was lself.h = ItemList(hl2[i])
                #~ lh.read() # -  zit al in __init__
                for x in range(lh.aantItems):
                    z = lh.Items[x]
                    slc = ""
                    if i == 0:
                        zk = rh.Userspec
                    elif i == 1:
                        zk = rh.Userspec
                    elif i == 2:
                        zk = rh.Functask
                    elif i == 3:
                        zk = rh.Funcproc
                    elif i == 4:
                        zk = rh.Funcdata
                    elif i == 5:
                        zk = rh.Techtask
                    elif i == 6:
                        zk = rh.Techproc
                    #~ elif i == 7:
                        #~ zk = rh.Techdata
                    elif i == 8:
                        zk = rh.Procproc
                    for y in zk:
                        if z == y:
                            slc = " selected"
                            break
                    hs = ('      <option%s value="%s">%s: %s</option>' % (slc,z[0],z[0],z[1]))
                    rgl.append(hs)
                rgl.append("    ")
        return rgl

class testcaller:
    def __init__(self):
        self.soort = "item"
        self.wat = "func" #
        self.cat = "proc"
        self.welk = "DocKies"
        self.proj = "1"
        self.zoek = "func_proc"
        self.wijzig = False
        if self.wijzig:
            self.fnaam = htmlpad + "input_" + self.wat + self.cat + ".html"
        elif self.wat == "start":
            self.fnaam = htmlpad + "start_proj.html"
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
        self.ok = True
        if not exists(self.fnaam):
            self.ok = False

def test():
    #~ proj = 1
    #~ for x in selector(1):
        #~ print x
    #~ return
    x = testcaller()
    if not x.ok:
        print x.fnaam,"bestaat niet"
        return
    s = printHTMLObject(x)
    if not s.ok:
        print "verkeerde soort opgegeven"
        return
    # test leesxml methode ---------------------------------------------
    #~ s.leesxml()
    #~ if s.dh.exists:
        #~ if soort == "userspec":
            #~ print ("%s %s: %s"% (soort,naam,s.dh.Kort))
        #~ elif soort == "funcproc":
            #~ print ("%s %s: %s"% (soort,naam,s.dh.Doel))
    #~ else:
        #~ print ("Geen informatie over %s %s"% (soort,naam))

    #~ # print s.rh.__dict__
    #~ if s.rh.exists:
        #~ for x in s.rh.__dict__:
            #~ if x in ["exists", "soort", "item", "fn", "fno"]:
                #~ continue
            #~ h = s.rh.__dict__[x]
            #~ if len(h) > 0:
                #~ print x,"relaties:"
                #~ for y in h:
                    #~ print y
    #~ else:
        #~ print ("Geen relaties bij %s %s"% (soort,naam))
    # test leeslist methode ----------------------------------------------
    #~ for x in s.leeslist():
      #~ print x
    # test toonxml methode ---------------------------------------------
    s.leesxml()
    l = s.toonxml()
    f = file(htmlpad + "test.html","w")
    for x in l:
      f.write("%s\n" % x)
    f.close()
    # test bouwregel methode ---------------------------------------------

if __name__ == '__main__':
    test()