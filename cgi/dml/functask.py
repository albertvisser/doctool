from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "func_task/"

class Functask(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"functask",procnaam,nieuw)
        self.Doel = ""
        self.Wanneer = []
        self.Wie = []
        self.Condities = []
        self.Waarvoor = []
        self.Beschrijving = []
        self.exists = False

    def nieuw(self):
        DocItem.nieuw(self,"functask")

    def read(self):
        DocItem.read(self)
        self.Doel = self.getPropText("doel")
        self.Wanneer = self.getPropList("wanneer")
        self.Wie = self.getPropList("wie")
        self.Waarvoor = self.getPropList("waarvoor")
        self.Condities = self.getPropList("condities")
        self.Beschrijving = self.getPropList("beschrijving")

    def write(self):
        self.setPropText("doel",self.Doel)
        self.setPropList("wanneer",self.Wanneer)
        self.setPropList("wie",self.Wie)
        self.setPropList("waarvoor",self.Waarvoor)
        self.setPropList("condities",self.Condities)
        self.setPropList("beschrijving",self.Beschrijving)
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
        print "Doel" + ih.Doel
        print "Wanneer: "
        for x in ih.Wanneer:
            print x
        print "Wie: "
        for x in ih.Wie:
            print x
        print "Waarvoor: "
        for x in ih.Waarvoor:
            print x
        print "Condities: "
        for x in ih.Condities:
            print x
        print "Beschrijving: "
        for x in ih.Beschrijving:
            print x

if __name__ == '__main__':
    from itemlist import ItemList
    lh = ItemList("functask")
    lh.read()
    test = lh.Items[0][1]
    ih = Functask(test)
    if ih.exists:
        ih.read()
        for x in ih.maakHtml():
            print x
    else:
        print test + " bestaat nog niet"

    #~ ih.wijzigDoel("Deze regel is zojuist toegevoegd aan Doel")
    #~ ih.addRegelToWanneer("Deze regel is zojuist toegevoegd aan Wanneer")
    #~ ih.addRegelToWie("Deze regel is zojuist toegevoegd aan Wie")
    #~ ih.addRegelToCondities("Deze regel is zojuist toegevoegd aan Condities")
    #~ ih.addRegelToWaarvoor("Deze regel is zojuist toegevoegd aan Waarvoor")
    #~ ih.addRegelToBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving")
    #~ printItem(test,ih)
    #~ ih.write()
    #~ ih.wijzigDoel("Deze regel is zojuist gewijzigd aan Doel")
    #~ ih.wijzigRegelInWanneer("Deze regel is zojuist toegevoegd aan Wanneer","Deze regel is zojuist gewijzigd aan Wanneer")
    #~ ih.wijzigRegelInWie("Deze regel is zojuist toegevoegd aan Wie","Deze regel is zojuist gewijzigd aan Wie")
    #~ ih.wijzigRegelInWaarvoor("Deze regel is zojuist toegevoegd aan Waarvoor","Deze regel is zojuist gewijzigd aan Waarvoor")
    #~ ih.wijzigRegelInCondities("Deze regel is zojuist toegevoegd aan Condities","Deze regel is zojuist gewijzigd aan Condities")
    #~ ih.wijzigRegelInBeschrijving("Deze regel is zojuist toegevoegd aan beschrijving","Deze regel is zojuist gewijzigd aan beschrijving")
    #~ printItem(test,ih)