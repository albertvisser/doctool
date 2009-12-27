from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "user_spec/"

class Userspec(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"userspec",procnaam,nieuw)
        self.Kort = ""
        self.Functie = []
        self.Beeld = []
        self.Product = []
        self.Omgeving = []

    def nieuw(self):
        DocItem.nieuw(self,"userspec")

    def read(self):
        DocItem.read(self)
        self.Kort = self.getPropText("kort")
        self.Functie = self.getPropList("functie")
        self.Beeld = self.getPropList("beeld")
        self.Product = self.getPropList("product")
        h1 = self.getSubPropText("kosten","omgeving")
        h2 = self.getSubPropText("baten","omgeving")
        self.Omgeving = [h1,h2] + self.getPropList("omgeving")

    def write(self):
        h = self.setPropText("kort",self.Kort)
        h = self.setPropList("functie",self.Functie)
        h = self.setPropList("beeld",self.Beeld)
        h = self.setPropList("product",self.Product)
        if len(self.Omgeving) == 0:
            h = self.setSubPropText("kosten","omgeving","")
            h = self.setSubPropText("baten","omgeving","")
            h = self.setPropList("omgeving",[])
        else:
            h = self.setSubPropText("kosten","omgeving",self.Omgeving[0])
            h = self.setSubPropText("baten","omgeving",self.Omgeving[1])
            h = self.setPropList("omgeving",self.Omgeving[2:])
        DocItem.write(self)
        if not self.exists: self.exists = True

    def wijzigKort(self,item):
        self.Kort = item

    def addRegelToFunctie(self,item):
        self.Functie.append(item)

    def wijzigRegelInFunctie(self,item,new):
        i = self.Functie.index(item)
        if new != item:
            self.Functie[i] = new

    def remRegelFromFunctie(self,item):
        try:
            self.Functie.remove(item)
        except:
            pass

    def addRegelToBeeld(self,item):
        self.Beeld.append(item)

    def wijzigRegelInBeeld(self,item,new):
        i = self.Beeld.index(item)
        if new != item:
            self.Beeld[i] = new

    def remRegelFromProduct(self,item):
        try:
            self.Product.remove(item)
        except:
            pass

    def addRegelToProduct(self,item):
        self.Product.append(item)

    def wijzigRegelInProduct(self,item,new):
        i = self.Product.index(item)
        if new != item:
            self.Product[i] = new

    def remRegelFromProduct(self,item):
        try:
            self.Product.remove(item)
        except:
            pass

    def addRegelToOmgeving(self,item):
        if len(self.Omgeving) == 0:
            self.Omgeving = ["",""]
        elif len(self.Omgeving) == 1:
            self.Omgeving.append("")
        self.Omgeving.append(item)

    def wijzigRegelInOmgeving(self,item,new):
        i = self.Omgeving.index(item)
        if new != item:
            self.Omgeving[i] = new

    def remRegelFromOmgeving(self,item):
        try:
            self.Omgeving.remove(item)
        except:
            pass

    def wijzigBaten(self,item):
        if len(self.Omgeving) == 0:
            self.Omgeving.append(item)
        else:
            self.Omgeving[0] = item

    def wijzigKosten(self,item):
        if len(self.Omgeving) == 0:
            self.Omgeving.append("")
            self.Omgeving.append(item)
        elif len(self.Omgeving) == 1:
            self.Omgeving.append(item)
        else:
            self.Omgeving[1] = item

    def printItem(self):
        print "Kort: " + self.Kort
        if len(ih.Functie) > 0:
            print "Functie: "
            for x in self.Functie:
                print x
        if len(self.Beeld) > 0:
            print 'Beeld: '
            for x in self.Beeld:
                print x
        if len(self.Product) > 0:
            print 'Uitvoer: '
            for x in self.Product:
                print x
        if len(self.Omgeving) > 0:
            print 'Omgeving: '
            i = 0
            for x in self.Omgeving:
                if i == 0:
                    print '    Baten: ' + x
                elif i == 1:
                    print '    Kosten: ' + x
                else:
                    print x
                i = i + 1

if __name__ == '__main__':
    test = "arargh"
    ih = Userspec(test)
    if ih.exists:
        print "-- na init --"
        print ih.__dict__
        ih.read()
        print "-- na read --"
        ih.printItem()
        #~ for x in ih.__dict__.keys():
            #~ print x,ih.__dict__[x]
    else:
        print test + " bestaat nog niet"
        ih.nieuw()
    ih.wijzigKort("Deze regel is zojuist toegevoegd aan kort")
    ih.addRegelToFunctie("Deze regel is zojuist toegevoegd aan functie")
    ih.addRegelToBeeld("Deze regel is zojuist toegevoegd aan beeld")
    ih.addRegelToProduct("Deze regel is zojuist toegevoegd aan product")
    ih.addRegelToOmgeving("Deze regel is zojuist toegevoegd aan omgeving")
    ih.wijzigBaten("Deze regel is zojuist toegevoegd aan de baten")
    ih.wijzigKosten("Deze regel is zojuist toegevoegd aan de kosten")
    ih.printItem()
    ih.write()
    #~ ih.wijzigRegelInKort("Deze regel is zojuist toegevoegd aan kort","Deze regel is zojuist gewijzigd aan kort")
    #~ ih.wijzigRegelInFunctie("Deze regel is zojuist toegevoegd aan functie","Deze regel is zojuist gewijzigd aan functie")
    #~ ih.wijzigRegelInBeeld("Deze regel is zojuist toegevoegd aan beeld","Deze regel is zojuist gewijzigd aan beeld")
    #~ ih.wijzigRegelInProduct("Deze regel is zojuist toegevoegd aan product","Deze regel is zojuist gewijzigd aan product")
    #~ ih.wijzigRegelInOmgeving("Deze regel is zojuist toegevoegd aan omgeving","Deze regel is zojuist gewijzigd aan omgeving")
    #~ ih.wijzigBaten("")
    #~ ih.wijzigKosten("")
    #~ printItem()
