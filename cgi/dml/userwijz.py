from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "user_wijz/"

class Userwijz(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False,project=0):
        DocItem.__init__(self,"userwijz",procnaam,nieuw)
        self.Wens = ""
        self.Nummer = procnaam
        self.Oplossing = []
        self.FuncAanv = []
        self.Realisatie = []
        self.TechAanv = []
        self.Opmerkingen = []
        self.BestondAl = False

    def nieuw(self):
        DocItem.nieuw(self,"userwijz")

    def read(self):
        DocItem.read(self)
        #~ self.Nummer = dh.Nummer.encode('ISO-8859-1')
        self.Wens = self.getPropText("wens")
        self.Oplossing = self.getPropList("oplossing")
        self.FuncAanv = self.getPropList("funcaanv")
        self.TechAanv = self.getPropList("techaanv")
        self.Realisatie = self.getPropList("realisatie")
        self.Opmerkingen = self.getPropList("opmerkingen")

    def write(self):
        self.getPropText("wens",self.Wens)
        self.getPropList("oplossing",self.Oplossing)
        self.getPropList("funcaanv",self.FuncAanv)
        self.getPropList("techaanv",self.TechAanv)
        self.getPropList("realisatie",self.Realisatie)
        self.getPropList("opmerkingen",self.Opmerkingen)
        DocItem.write(self)
        if not self.exists: self.exists = True

    def wijzigNummer(self,item):
        self.Nummer = item

    def wijzigWens(self,item):
        self.Wens = item

    def addRegelToOplossing(self,item):
        self.Oplossing.append(item)

    def wijzigRegelInOplossing(self,item,new):
        i = self.Oplossing.index(item)
        if new != item:
            self.Oplossing[i] = new

    def remRegelFromOplossing(self,item):
        try:
            self.Oplossing.remove(item)
        except:
            pass

    def addRegelToFuncAanv(self,item):
        self.FuncAanv.append(item)

    def wijzigRegelInFuncAanv(self,item,new):
        i = self.FuncAanv.index(item)
        if new != item:
            self.FuncAanv[i] = new

    def remRegelFromFuncAanv(self,item):
        try:
            self.FuncAanv.remove(item)
        except:
            pass

    def addRegelToTechAanv(self,item):
        self.TechAanv.append(item)

    def wijzigRegelInTechAanv(self,item,new):
        i = self.TechAanv.index(item)
        if new != item:
            self.TechAanv[i] = new

    def remRegelFromTechAanv(self,item):
        try:
            self.TechAanv.remove(item)
        except:
            pass

    def addRegelToRealisatie(self,item):
        self.Realisatie.append(item)

    def wijzigRegelInRealisatie(self,item,new):
        i = self.Realisatie.index(item)
        if new != item:
            self.Realisatie[i] = new

    def remRegelFromRealisatie(self,item):
        try:
            self.Realisatie.remove(item)
        except:
            pass

    def addRegelToOpmerkingen(self,item):
        self.Opmerkingen.append(item)

    def wijzigRegelInOpmerkingen(self,item,new):
        i = self.Opmerkingen.index(item)
        if new != item:
            self.Opmerkingen[i] = new

    def remRegelFromOpmerkingen(self,item):
        try:
            self.Opmerkingen.remove(item)
        except:
            pass

    def printItem(self):
        print 'Wens:', self.Wens
        print 'Gekozen/gesuggereerde oplossing:'
        if len(self.Oplossing) > 0:
            for x in self.Oplossing:
                print " ", x
        print 'Opmerkingen van functionele aard :'
        if len(self.FuncAanv) > 0:
            for x in self.FuncAanv:
                print " ", x
        print 'Opmerkingen van technische aard:'
        if len(self.TechAanv) > 0:
            for x in self.TechAanv:
                print " ", x
        print 'Opmerkingen m.b.t. realisatie:'
        if len(self.Realisatie) > 0:
            for x in self.Realisatie:
                print " ", x
        print 'Overige opmerkingen:'
        if len(self.Opmerkingen) > 0:
            for x in self.Opmerkingen:
                print " ", x
        #~ return s

def test_1(vervolg=False):
    # lees alle userwijz items
    from itemlist import ItemList
    lh = ItemList("userwijz","0")
    lh.read()
    if vervolg:
        return lh.Items[0][1]
    else:
        if len(lh.Items) > 0:
            print "nummer  titel  omschrijving"
            for x in lh.Items:
                print x[0],x[1],x[2]
        else:
            print "nog geen userwijzs"

def test_2(test):
    # lees de aangegeven wens en toon de inhoud in html-opmaak
    ih = Userwijz(test)
    if ih.exists:
        ih.read()
        #~ ih.printItem()
        for x in ih.maakHtml():
            print x
    else:
        print ("'%s' bestaat nog niet" % test)
        print ih.__dict__

def test_3(test):
    # probeer een nieuw item op te voeren
    nieuw = True
    ih = Userwijz(test,nieuw)
    if ih.BestondAl:
        print ("'%s' bestaat al, bedenk een nieuwe naam" % test)
    else:
        ih.read()
        #~ ih.printItem()
        for x in ih.maakHtml():
            print x

def test_4(test):
    # properties opvoeren
    ih = Userwijz(test)
    if ih.exists:
        ih.read()
        print "--- na eerste lees ---"
        ih.printItem()
        ih.wijzigWens("Deze regel is zojuist toegevoegd aan Wens")
        ih.addRegelToOplossing("Deze regel is zojuist toegevoegd aan Oplossing")
        ih.addRegelToFuncAanv("Deze regel is zojuist toegevoegd aan FuncAanv")
        ih.addRegelToRealisatie("Deze regel is zojuist toegevoegd aan Realisatie")
        ih.addRegelToTechAanv("Deze regel is zojuist toegevoegd aan TechAanv")
        ih.addRegelToOpmerkingen("Deze regel is zojuist toegevoegd aan opmerkingen")
        print "--- na instellen properties ---"
        ih.printItem()
        ih.write()
        ih.read()
        print "--- na tweede lees na schrijven ---"
        ih.printItem()
    else:
        print ("niks gedaan, '%s' bestaat nog niet" % test)

def test_5(test):
    # properties wijzigen
    ih = Userwijz(test)
    if ih.exists:
        ih.read()
        print "--- na eerste lees ---"
        ih.printItem()
        ih.wijzigWens("Deze regel is zojuist gewijzigd aan Wens")
        ih.wijzigRegelInOplossing("Deze regel is zojuist toegevoegd aan Oplossing","Deze regel is zojuist gewijzigd aan Oplossing")
        ih.wijzigRegelInFuncAanv("Deze regel is zojuist toegevoegd aan FuncAanv","Deze regel is zojuist gewijzigd aan FuncAanv")
        ih.wijzigRegelInTechAanv("Deze regel is zojuist toegevoegd aan TechAanv","Deze regel is zojuist gewijzigd aan TechAanv")
        ih.wijzigRegelInRealisatie("Deze regel is zojuist toegevoegd aan Realisatie","Deze regel is zojuist gewijzigd aan Realisatie")
        ih.wijzigRegelInOpmerkingen("Deze regel is zojuist toegevoegd aan opmerkingen","Deze regel is zojuist gewijzigd aan opmerkingen")
        print "--- na instellen properties ---"
        ih.printItem()
        ih.write()
        ih.read()
        print "--- na tweede lees na schrijven ---"
        ih.printItem()
    else:
        print ("niks gedaan, '%s' bestaat nog niet" % test)

def test():
    #~ vervolg = True
    #~ test = test_1(vervolg)
    test = "nieuw iets"
    test_5(test)
    return

if __name__ == '__main__':
    test()