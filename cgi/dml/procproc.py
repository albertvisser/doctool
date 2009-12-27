from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "proc_proc/"

class Procproc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"procproc",procnaam,nieuw)
        self.Titel = ""
        self.Doel = ""
        self.Invoer = []
        self.Uitvoer = []
        self.Werkwijze = []
        self.Bijzonder = []
        self.Hoetetesten = []
        self.Testgevallen = []

    def nieuw(self):
        DocItem.nieuw(self,"procproc")

    def read(self):
        DocItem.read(self)
        self.Titel = self.getPropText("titel")
        self.Doel = self.getPropText("doel")
        self.Invoer = self.getPropList("invoer")
        self.Uitvoer = self.getPropList("uitvoer")
        self.Werkwijze = self.getPropList("werkwijze")
        self.Bijzonder = self.getPropList("bijzonder")
        self.Hoetetesten = self.getPropList("hoetetesten")
        self.Testgevallen = self.getPropList("testgevallen")

    def write(self):
        self.setPropText("titel",self.Titel)
        self.setPropText("doel",self.Doel)
        self.setPropList("invoer",self.Invoer)
        self.setPropList("uitvoer",self.Uitvoer)
        self.setPropList("werkwijze",self.Werkwijze)
        self.setPropList("bijzonder",self.Bijzonder)
        self.setPropList("hoetetesten",self.Hoetetesten)
        self.setPropList("testgevallen",self.Testgevallen)
        DocItem.write(self)
        if not self.exists: self.exists = True

    def wijzigTitel(self,item):
        self.Titel = item

    def wijzigDoel(self,item):
        self.Doel = item

    def addRegelToInvoer(self,item):
        self.Invoer.append(item)

    def wijzigRegelInInvoer(self,item,new):
        i = self.Invoer.index(item)
        if new != item:
            self.Invoer[i] = new

    def remRegelFromInvoer(self,item):
        try:
            self.Invoer.remove(item)
        except:
            pass

    def addRegelToUitvoer(self,item):
        self.Uitvoer.append(item)

    def wijzigRegelInUitvoer(self,item,new):
        i = self.Uitvoer.index(item)
        if new != item:
            self.Uitvoer[i] = new

    def remRegelFromUitvoer(self,item):
        try:
            self.Uitvoer.remove(item)
        except:
            pass

    def addRegelToWerkwijze(self,item):
        self.Werkwijze.append(item)

    def wijzigRegelInWerkwijze(self,item,new):
        i = self.Werkwijze.index(item)
        if new != item:
            self.Werkwijze[i] = new

    def remRegelFromWerkwijze(self,item):
        try:
            self.Werkwijze.remove(item)
        except:
            pass

    def addRegelToBijzonder(self,item):
        self.Bijzonder.append(item)

    def wijzigRegelInBijzonder(self,item,new):
        i = self.Bijzonder.index(item)
        if new != item:
            self.Bijzonder[i] = new

    def remRegelFromBijzonder(self,item):
        try:
            self.Bijzonder.remove(item)
        except:
            pass

    def addRegelToHoetetesten(self,item):
        self.Hoetetesten.append(item)

    def wijzigRegelInHoetetesten(self,item,new):
        i = self.Hoetetesten.index(item)
        if new != item:
            self.Hoetetesten[i] = new

    def remRegelFromHoetetesten(self,item):
        try:
            self.Hoetetesten.remove(item)
        except:
            pass

    def addRegelToTestgevallen(self,item):
        self.Testgevallen.append(item)

    def wijzigRegelInTestgevallen(self,item,new):
        i = self.Testgevallen.index(item)
        if new != item:
            self.Testgevallen[i] = new

    def remRegelFromTestgevallen(self,item):
        try:
            self.Testgevallen.remove(item)
        except:
            pass

    def printItem(self,test):
        print ("====== object: %s ==========" % test)
        print "Titel" + self.Titel
        print "Doel" + self.Doel
        print "Invoer: "
        for x in self.Invoer:
            print x
        print "Uitvoer: "
        for x in self.Uitvoer:
            print x
        print "Werkwijze: "
        for x in self.Werkwijze:
            print x
        print "Bijzonder: "
        for x in self.Bijzonder:
            print x
        print "Hoetetesten: "
        for x in self.Hoetetesten:
            print x
        print "Testgevallen: "
        for x in self.Testgevallen:
            print x

if __name__ == '__main__':
    from itemlist import ItemList
    lh = ItemList("procproc")
    lh.read()
    if len(lh.Items) > 0:
        test = lh.Items[0][1]
        ih = Funcproc(test)
        if ih.exists:
            ih.read()
            for x in ih.maakHtml():
                print x
        else:
            print test + " bestaat nog niet"
    else:
        print "Nog geen lijst met procedurebeschrijvingen"
    #~ printItem(test,ih)
    #~ ih.wijzigTitel("Deze regel is zojuist toegevoegd aan Titel")
    #~ ih.wijzigDoel("Deze regel is zojuist toegevoegd aan Doel")
    #~ ih.addRegelToInvoer("Deze regel is zojuist toegevoegd aan invoer")
    #~ ih.addRegelToUitvoer("Deze regel is zojuist toegevoegd aan uitvoer")
    #~ ih.addRegelToWerkwijze("Deze regel is zojuist toegevoegd aan werkwijze")
    #~ ih.addRegelToBijzonder("Deze regel is zojuist toegevoegd aan bijzonder")
    #~ ih.addRegelToWerkwijze("Deze regel is zojuist toegevoegd aan werkwijze")
    #~ ih.addRegelToWerkwijze("Deze regel is zojuist toegevoegd aan werkwijze")
    #~ printItem(test,ih)
    #~ ih.wijzigTitel("Deze regel is zojuist gewijzigd aan Titel")
    #~ ih.wijzigDoel("Deze regel is zojuist gewijzigd aan Doel")
    #~ ih.wijzigRegelInInvoer("Deze regel is zojuist toegevoegd aan invoer","Deze regel is zojuist gewijzigd aan invoer")
    #~ ih.addRegelToInvoer("Deze regel is zojuist toegevoegd aan invoer")
    #~ ih.wijzigRegelInUitvoer("Deze regel is zojuist toegevoegd aan uitvoer","Deze regel is zojuist gewijzigd aan uitvoer")
    #~ ih.addRegelToUitvoer("Deze regel is zojuist toegevoegd aan uitvoer")
    #~ ih.wijzigRegelInWerkwijze("Deze regel is zojuist toegevoegd aan werkwijze","Deze regel is zojuist gewijzigd aan werkwijze")
    #~ ih.addRegelToWerkwijze("Deze regel is zojuist toegevoegd aan werkwijze")
    #~ ih.wijzigRegelInBijzonder("Deze regel is zojuist toegevoegd aan bijzonder","Deze regel is zojuist gewijzigd aan bijzonder")
    #~ ih.addRegelToBijzonder("Deze regel is zojuist toegevoegd aan bijzonder")
    #~ ih.wijzigRegelInHoetetesten("Deze regel is zojuist toegevoegd aan hoetetesten","Deze regel is zojuist gewijzigd aan hoetetesten")
    #~ ih.addRegelToHoetetesten("Deze regel is zojuist toegevoegd aan hoetetesten")
    #~ ih.wijzigRegelInTestgevallen("Deze regel is zojuist toegevoegd aan testgevallen","Deze regel is zojuist gewijzigd aan testgevallen")
    #~ ih.addRegelToTestgevallen("Deze regel is zojuist toegevoegd aan testgevallen")
    #~ printItem(test,ih)