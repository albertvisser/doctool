from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "tech_task/"

class Techtask(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"techtask",procnaam,nieuw)
        self.Kort = ""
        self.Doel = []
        self.Periode = []
        self.Verloop = []

    def nieuw(self):
        DocItem.nieuw(self,"techtask")

    def read(self):
        DocItem.read(self)
        self.Kort = self.getPropText("kort")
        self.Doel = self.getPropList("doel")
        self.Periode = self.getPropList("periode")
        self.Verloop = self.getPropList("verloop")

    def write(self):
        self.setPropText("kort",self.Kort)
        self.setPropList("doel",self.Doel)
        self.setPropList("periode",self.Periode)
        self.setPropList("verloop",self.Verloop)
        DocItem.write(self)
        if not self.exists: self.exists = True

    def wijzigKort(self,item):
        self.Kort = item

    def addRegelToDoel(self,item):
        self.Doel.append(item)

    def wijzigRegelInDoel(self,item,new):
        i = self.Doel.index(item)
        if new != item:
            self.Doel[i] = new

    def remRegelFromDoel(self,item):
        try:
            self.Doel.remove(item)
        except:
            pass

    def addRegelToPeriode(self,item):
        self.Periode.append(item)

    def wijzigRegelInPeriode(self,item,new):
        i = self.Periode.index(item)
        if new != item:
            self.Periode[i] = new

    def remRegelFromPeriode(self,item):
        try:
            self.Periode.remove(item)
        except:
            pass

    def addRegelToVerloop(self,item):
        self.Verloop.append(item)

    def wijzigRegelInVerloop(self,item,new):
        i = self.Verloop.index(item)
        if new != item:
            self.Verloop[i] = new

    def remRegelFromVerloop(self,item):
        try:
            self.Verloop.remove(item)
        except:
            pass

    def printItem(self, test):
        print ("====== object: %s ==========" % test)
        print "Kort" + self.Kort
        print "Doel: "
        for x in self.Doel:
            print x
        print "Periode: "
        for x in self.Periode:
            print x
        print "Verloop: "
        for x in self.Verloop:
            print x

if __name__ == '__main__':
    from itemlist import ItemList
    lh = ItemList("techtask")
    lh.read()
    test = lh.Items[0][1]
    ih = Techtask(test)
    if ih.exists:
        ih.read()
        for x in ih.maakHtml():
            print x
    else:
        print test + " bestaat nog niet"
    #~ printItem(test,ih)
    #~ ih.wijzigKort("Deze regel is zojuist toegevoegd aan Kort")
    #~ ih.addRegelToDoel("Deze regel is zojuist toegevoegd aan Doel")
    #~ ih.addRegelToPeriode("Deze regel is zojuist toegevoegd aan Periode")
    #~ ih.addRegelToVerloop("Deze regel is zojuist toegevoegd aan Verloop")
    #~ printItem(test,ih)
    #~ ih.wijzigKort("Deze regel is zojuist gewijzigd aan Kort")
    #~ ih.wijzigRegelInDoel("Deze regel is zojuist toegevoegd aan Doel","Deze regel is zojuist gewijzigd aan Doel")
    #~ ih.addRegelToDoel("Deze regel is zojuist toegevoegd aan Doel")
    #~ ih.wijzigRegelInPeriode("Deze regel is zojuist toegevoegd aan Periode","Deze regel is zojuist gewijzigd aan Periode")
    #~ ih.addRegelToPeriode("Deze regel is zojuist toegevoegd aan Periode")
    #~ ih.wijzigRegelInVerloop("Deze regel is zojuist toegevoegd aan Verloop","Deze regel is zojuist gewijzigd aan Verloop")
    #~ ih.addRegelToVerloop("Deze regel is zojuist toegevoegd aan Verloop")
    #~ printItem(test,ih)