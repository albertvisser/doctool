from collections import OrderedDict
from docitems import DocItem

class Project(DocItem):
    "lijst alle gegegevsn van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "project", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ('kort', {"type": 'text'}),
            ('oms', {"type": 'text'}),
            ('start', {"type": 'text'}),
            ('fysloc', {"type": 'text'}),
            ('status', {"type": 'text'}),
            ])

class Userspec(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self, "userspec", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("kort", {"type": 'text'}),
            ("functie", {"type": 'list'}),
            ("beeld", {"type": 'list'}),
            ("product", {"type": 'list'}),
            ("kosten", {"type": 'prop', 'pad': "omgeving"}),
            ("baten", {"type": 'prop', 'pad': "omgeving"}),
            ("omgeving", {"type": 'list'}),
            ])

class UserDoc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "userdoc", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("link", {'type': "attr", 'naam': 'url'}),
            ("tekst", {'type': "list", })
            ])

class Userwijz(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False, project=0):
        DocItem.__init__(self, "userwijz", procnaam, nieuw)
        self.prpnames = OrderedDict([
            #~ self.Nummer = dh.Nummer.encode('ISO-8859-1')
            ("wens", {"type": 'text'}),
            ("oplossing", {"type": 'list'}),
            ("funcaanv", {"type": 'list'}),
            ("techaanv", {"type": 'list'}),
            ("realisatie", {"type": 'list'}),
            ("opmerkingen", {"type": 'list'}),
            ])

class Functask(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "functask", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("doel", {"type": 'text'}),
            ("wanneer", {"type": 'list'}),
            ("wie", {"type": 'list'}),
            ("waarvoor", {"type": 'list'}),
            ("condities", {"type": 'list'}),
            ("beschrijving", {"type": 'list'}),
            ])

class Funcproc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "funcproc", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("doel",  {"type": 'text'}),
            ("invoer", {"type": 'list'}),
            ("uitvoer", {"type": 'list'}),
            ("wanneer", {"type": 'list'}),
            ("wie", {"type": 'list'}),
            ("waarvoor",  {"type": 'list'}),
            ("condities",  {"type": 'list'}),
            ("beschrijving",  {"type": 'list'}),
            ])

class FuncDoc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "funcdocs", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("link", {'type': "attr", 'naam': 'url'}),
            ("tekst", {'type': "list", })
            ])

## class Entiteit(DocItem):
    ## "lijst alle gegevens van een bepaald item"
    ## def __init__(self, naam, nieuw=False):
        ## DocItem.__init__(self, "entiteit", procnaam, nieuw)
        ## self.prpnames = OrderedDict([
            ## (, {"type": }),
            ## ])
        ## self.Naam = self.getPropText("naam")
        ## self.Functie = self.getPropText("functie")
        ## self.Attribuut = self.getAttribuut()
        ## # subelement opbouw (1)
          ## # subelement attribuut  (0-n)
            ## # attribuut naam
            ## # attribuut jaar
            ## # subelement omschrijving: text
            ## # subelement bijzonderheden: text
        ## self.Toegang = self.getToegang()
        ## # subelement toegang (1-n)
          ## # attribuut naam
          ## # attribuut volgorde
        ## self.Relatie = self.getRelaties()
        ## # subelement relatie (0-n)
          ## # attribuut naam
          ## # attribuut  entiteit
          ## # (attribuut volgorde)
        ## self.Levensloop = self.getPropList("levensloop")
    ## def getAttribuut(self):
        ## h = self.root.find("opbouw")
        ## if h is None:
            ## h = []
        ## else:
            ## hh = h.findall("attribuut")
            ## h = []
            ## for x in hh:
                ## i = [x.get("naam"),x.get("type")]
                ## t = x.find("omschrijving")
                ## if t is not None:
                    ## i.append(t.text)
                ## else:
                    ## i.append("")
                ## t = x.find("bijzonderheden")
                ## if t is not None:
                    ## i.append(t.text)
                ## else:
                    ## i.append("")
                ## h.append(i)
        ## return h

    ## def getToegang(self):
        ## h = {}
        ## for x in self.root.findall("toegang"):
            ## h[x.get("naam")] = x.get("volgorde")
        ## return h

    ## def getRelaties(self):
        ## h = {}
        ## for x in self.root.findall("relatie"):
            ## h[x.get("naam")] = x.get("entiteit")
        ## return h

class Techtask(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "techtask", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("kort", {'type': "text", }),
            ("doel", {'type': "list", }),
            ("periode", {'type': "list", }),
            ("verloop", {'type': "list", }),
            ])

class Techproc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "techproc", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ("titel", {'type': "text", }),
            ("doel", {'type': "text", }),
            ("invoer", {'type': "list", }),
            ("uitvoer", {'type': "list", }),
            ("beschrijving", {'type': "list", })
            ])

class DataItem(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam, nieuw=False):
        DocItem.__init__(self, "techproc", procnaam, nieuw)
        self.prpnames = OrderedDict([
            ## <!ELEMENT gegevens (functie,opbouw,toegang,relatie,levensloop)>
            ## <!ELEMENT functie (#PCDATA)>
            ## <!ELEMENT opbouw  (attribuut+)>
            ## <!ELEMENT attribuut	(omschrijving, soort)>
            ## <!ATTLIST attribuut naam CDATA #REQUIRED soort CDATA #REQUIRED>
            ## <!ELEMENT omschrijving (#PCDATA)>
            ## <!ELEMENT soort (#PCDATA)>
            ## <!ELEMENT toegang (EMPTY)>
            ## <!ATTLIST toegang naam CDATA #REQUIRED>
            ## <!ELEMENT relatie (EMPTY)>
            ## <!ATTLIST relatie naam CDATA #REQUIRED entiteit CDATA #REQUIRED)>
            ## <!ELEMENT levensloop (regel*)>
            ## <!ELEMENT regel (#PCDATA)>
            ])

class Procproc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"procproc",procnaam,nieuw)
        self.prpnames = OrderedDict([
            ("titel", {'type': "text", }),
            ("doel", {'type': "text", }),
            ("invoer", {'type': "list", }),
            ("uitvoer", {'type': "list", }),
            ("werkwijze", {'type': "list", }),
            ("bijzonder", {'type': "list", }),
            ("hoetetesten", {'type': "list", }),
            ("testgevallen", {'type': "list", }),
            ])
