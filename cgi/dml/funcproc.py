from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "func_proc/"

class Funcproc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"funcproc",procnaam,nieuw)
        self.Doel = ""
        self.Wanneer = []
        self.Wie = []
        self.Condities = []
        self.Waarvoor = []
        self.Invoer = []
        self.Uitvoer = []
        self.Beschrijving = []

    def nieuw(self):
        DocItem.nieuw(self,"funcproc")

    def read(self):
        DocItem.read(self)
        self.Doel = self.getPropText("doel")
        self.Invoer = self.getPropList("invoer")
        self.Uitvoer = self.getPropList("uitvoer")
        self.Wanneer = self.getPropList("wanneer")
        self.Wie = self.getPropList("wie")
        self.Waarvoor = self.getPropList("waarvoor")
        self.Condities = self.getPropList("condities")
        self.Beschrijving = self.getPropList("beschrijving")

    def write(self):
        self.getPropText("doel",self.Doel)
        self.getPropList("invoer",self.Invoer)
        self.getPropList("uitvoer",self.Uitvoer)
        self.getPropList("wanneer",self.Wanneer)
        self.getPropList("wie",self.Wie)
        self.getPropList("waarvoor",self.Waarvoor)
        self.getPropList("condities",self.Condities)
        self.getPropList("beschrijving",self.Beschrijving)
        DocItem.write(self)
        if not self.exists: self.exists = True

    def wijzigDoel(self,item):
        self.Doel = item

    def addRegelToWanneer(self,item):
        self.Wanneer.append(item)

    def wijzigRegelInWanneer(self,item,new):
        i = self.Wanneer.index(item)
        if new != item:
            self.Wanneer[i] = new

    def remRegelFromWanneer(self,item):
        try:
            self.Wanneer.remove(item)
        except:
            pass

    def addRegelToWie(self,item):
        self.Wie.append(item)

    def wijzigRegelInWie(self,item,new):
        i = self.Wie.index(item)
        if new != item:
            self.Wie[i] = new

    def remRegelFromWie(self,item):
        try:
            self.Wie.remove(item)
        except:
            pass

    def addRegelToWaarvoor(self,item):
        self.Waarvoor.append(item)

    def wijzigRegelInWaarvoor(self,item,new):
        i = self.Waarvoor.index(item)
        if new != item:
            self.Waarvoor[i] = new

    def remRegelFromWaarvoor(self,item):
        try:
            self.Waarvoor.remove(item)
        except:
            pass

    def addRegelToCondities(self,item):
        self.Condities.append(item)

    def wijzigRegelInCondities(self,item,new):
        i = self.Condities.index(item)
        if new != item:
            self.Condities[i] = new

    def remRegelFromCondities(self,item):
        try:
            self.Condities.remove(item)
        except:
            pass

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

    def printItem(self,test):
        print ("====== object: %s ==========" % test)
        print "Doel" + self.Doel
        print "Wanneer:"
        for x in self.Wanneer:
            print x
        print "Wie:"
        for x in self.Wie:
            print x
        print "Waarvoor:"
        for x in self.Waarvoor:
            print x
        print "Invoer: "
        for x in self.Invoer:
            print x
        print "Wie:"
        for x in self.Wie:
            print x
        print "Condities: "
        for x in self.Condities:
            print x
        print "Beschrijving: "
        for x in self.Beschrijving:
            print x

if __name__ == '__main__':
    from itemlist import ItemList
    lh = ItemList("funcproc")
    lh.read()
    test = lh.Items[0][1]
    ih = Funcproc(test)
    if ih.exists:
        ih.read()
        for x in ih.maakHtml():
            print x
    else:
        print test + " bestaat nog niet"
    #~ printItem(test,ih)
    #~ ih.wijzigDoel("Deze regel is zojuist toegevoegd aan Doel")
    #~ ih.addRegelToWanneer("Deze regel is zojuist toegevoegd aan Wanneer")
    #~ ih.addRegelToWie("Deze regel is zojuist toegevoegd aan Wie")
    #~ ih.addRegelToCondities("Deze regel is zojuist toegevoegd aan Condities")
    #~ ih.addRegelToWaarvoor("Deze regel is zojuist toegevoegd aan Waarvoor")
    #~ ih.addRegelToInvoer("Deze regel is zojuist toegevoegd aan invoer")
    #~ ih.addRegelToUitvoer("Deze regel is zojuist toegevoegd aan uitvoer")
    #~ ih.addRegelToBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving")
    #~ printItem(test,ih)
    #~ ih.wijzigDoel("Deze regel is zojuist gewijzigd aan Doel")
    #~ ih.wijzigRegelInWanneer("Deze regel is zojuist toegevoegd aan Wanneer","Deze regel is zojuist gewijzigd aan Wanneer")
    #~ ih.wijzigRegelInWie("Deze regel is zojuist toegevoegd aan Wie","Deze regel is zojuist gewijzigd aan Wie")
    #~ ih.wijzigRegelInWaarvoor("Deze regel is zojuist toegevoegd aan Waarvoor","Deze regel is zojuist gewijzigd aan Waarvoor")
    #~ ih.wijzigRegelInCondities("Deze regel is zojuist toegevoegd aan Condities","Deze regel is zojuist gewijzigd aan Condities")
    #~ ih.wijzigRegelInInvoer("Deze regel is zojuist toegevoegd aan invoer","Deze regel is zojuist gewijzigd aan invoer")
    #~ ih.wijzigRegelInUitvoer("Deze regel is zojuist toegevoegd aan uitvoer","Deze regel is zojuist gewijzigd aan uitvoer")
    #~ ih.wijzigRegelInBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving","Deze regel is zojuist gewijzigd aan beschrijving")
    #~ printItem(test,ih)