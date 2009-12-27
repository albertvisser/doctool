from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "tech_proc/"

class Techproc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"techproc",procnaam,nieuw)
        self.Titel = ""
        self.Doel = ""
        self.Invoer = []
        self.Uitvoer = []
        self.Beschrijving = []
        self.Omgeving = []

    def nieuw(self, type="techproc"):
        DocItem.nieuw(self,type)

    def read(self):
        DocItem.read(self)
        self.Titel = self.getPropText("titel")
        self.Doel = self.getPropText("doel")
        self.Invoer = self.getPropList("invoer")
        self.Uitvoer = self.getPropList("uitvoer")
        self.Beschrijving = self.getPropList("beschrijving")

    def write(self):
        self.setPropText("titel",self.Titel )
        self.setPropText("doel",self.Doel)
        self.setPropList("invoer",self.Invoer)
        self.setPropList("uitvoer",self.Uitvoer)
        self.setPropList("beschrijving",self.Beschrijving)
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

    def remRegelFromBeschrijving(self,item):
        try:
            self.Beschrijving.remove(item)
        except:
            pass

    def addRegelToBeschrijving(self,item):
        self.Beschrijving.append(item)

    def wijzigRegelInBeschrijving(self,item,new):
        i = self.Beschrijving.index(item)
        if new != item:
            self.Beschrijving[i] = new

    def remRegelFromBeschrijving(self,item):
        try:
            self.Beschrijving.remove(item)
        except:
            pass

    def printItem(test, ih):
        print ("====== object: %s ==========" % test)
        print "Titel" + ih.Titel
        print "Doel" + ih.Doel
        print "Invoer: "
        for x in ih.Invoer:
            print x
        print "Uitvoer: "
        for x in ih.Uitvoer:
            print x
        print "Beschrijving: "
        for x in ih.Beschrijving:
            print x


if __name__ == '__main__':
    from itemlist import ItemList
    lh = ItemList("techproc")
    lh.read()
    test = lh.Items[0][1]
    ih = Techproc(test)
    if ih.exists:
        ih.read()
        for x in ih.maakHtml():
            print x
    else:
        print test + " bestaat nog niet"
    #~ printItem(test,ih)
    #~ ih.wijzigTitel("Deze regel is zojuist toegevoegd aan Titel")
    #~ ih.wijzigDoel("Deze regel is zojuist toegevoegd aan Doel")
    #~ ih.addRegelToInvoer("Deze regel is zojuist toegevoegd aan invoer")
    #~ ih.addRegelToUitvoer("Deze regel is zojuist toegevoegd aan uitvoer")
    #~ ih.addRegelToBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving")
    #~ printItem(test,ih)
    #~ ih.wijzigTitel("Deze regel is zojuist gewijzigd aan Titel")
    #~ ih.wijzigDoel("Deze regel is zojuist gewijzigd aan Doel")
    #~ ih.wijzigRegelInInvoer("Deze regel is zojuist toegevoegd aan invoer","Deze regel is zojuist gewijzigd aan invoer")
    #~ ih.addRegelToInvoer("Deze regel is zojuist toegevoegd aan invoer")
    #~ ih.wijzigRegelInUitvoer("Deze regel is zojuist toegevoegd aan uitvoer","Deze regel is zojuist gewijzigd aan uitvoer")
    #~ ih.addRegelToUitvoer("Deze regel is zojuist toegevoegd aan uitvoer")
    #~ ih.wijzigRegelInBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving","Deze regel is zojuist gewijzigd aan beschrijving")
    #~ ih.addRegelToBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving")
    #~ printItem(test,ih)
