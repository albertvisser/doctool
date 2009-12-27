from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "user_docs/"

class UserDoc(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, procnaam,nieuw=False):
        DocItem.__init__(self,"userdoc",procnaam,nieuw)
        self.Link = ""
        self.Tekst = []

    def nieuw(self):
        DocItem.nieuw(self,"userdoc")

    def read(self):
        DocItem.read(self)
        self.Link = self.getPropText("link")
        self.Tekst = self.getPropList("tekst")

    def write(self):
        self.setPropText("link",self.Link)
        self.setPropList("tekst",self.Tekst)
        DocItem.write(self)
        if not self.exists: self.exists = True

    def setProp(self,name,value):
        if name == "link":
            if type(value) is str:
                h = self.root.find(name)
                if h is None:
                    h = SubElement(self.root,name)
                h.set("url",value)
            else:
                raise DataError("link attribuut moet string zijn")
        elif name == "tekst":
            if type(value) is list or tuple:
                h = self.root.find(name)
                if h is not None:
                    self.root.remove(h)
                h = SubElement(self.root,name)
                for x in value:
                    hh = SubElement(h,"regel")
                    hh.text = x
            else:
                raise DataError("tekst attribuut moet list of tuple zijn")
        else:
            raise DataError("onbekend attribuut")

    def getProp(self,name):
        if name == "link":
            h = self.root.find(name)
            if h is None:
                h = ""
            else:
                hh = h.get("url")
                if hh is None:
                    h = ""
                else:
                    h = hh
        elif name == "tekst":
            h = self.root.find(name)
            if h is None:
                h = []
            else:
                hh = h.findall("regel")
                h = []
                for x in hh:
                    if x.text is None:
                        h.append("")
                    else:
                        h.append(x.text)
        return h

    def wijzigLink(self,item):
        self.Link = item

    def wijzigTekst(self,item):
        if type(item) is list or tuple:
            self.Tekst = item

    def addRegelToTekst(self,item):
        self.Tekst.append(item)

    def wijzigRegelInTekst(self,item,new):
        i = self.Tekst.index(item)
        if new != item:
            self.Tekst[i] = new

    def delRegelFromTekst(self,item):
        try:
            self.Tekst.remove(item)
        except:
            pass

    def printItem(self):
        print "Link: " + self.Link
        if len(ih.Tekst) > 0:
            print "Tekst: "
            for x in self.Tekst:
                print x

if __name__ == '__main__':
    #~ test = "demo"
    test = "lifecycle"
    ih = UserDoc(test)
    if ih.exists:
        ih.read()
        print "Na read: ---------------"
        print ih.__dict__
        ih.printItem()
        #~ ih.wijzigRegelInTekst("Geen familie helaas","Daar bij die molen")
        #~ print "Na wijzigregel: ---------------"
        #~ ih.printItem()
        #~ ih.addRegelToTekst("In het gebosschte verscholen")
        #~ print "Na addregel: ---------------"
        #~ ih.printItem()
        #~ ih.delRegelFromTekst("")
        #~ print "Na delregel: ---------------"
        #~ ih.printItem()
        #~ ih.wijzigLink("H:\\Snorkesteijn\\Niks aan de hand.doc")
        #~ print "Na wijziglink: ---------------"
        #~ ih.printItem()
        #~ ih.wijzigtekst(["Er was eens een man","Toeluisterdan","Er was eens een vrouw","Toeluisternou","","Geen familie helaas"])
        #~ print "Na wijzigtekst: ---------------"
        #~ ih.printItem()
        #~ ih.write()
    else:
        #~ print test + " bestaat nog niet"
        ih.nieuw()
        print "Na nieuw: ---------------"
        ih.printItem()
        ih.wijzigLink("testlink")
        print "Na wijziglink: ---------------"
        ih.printItem()
        ih.wijzigtekst(["hallo"])
        print "Na wijzigtekst: ---------------"
        ih.printItem()
        ih.write()
    #~ ih.addRegelToKort("Deze regel is zojuist toegevoegd aan kort")
    #~ ih.addRegelToFunctie("Deze regel is zojuist toegevoegd aan functie")
    #~ ih.addRegelToBeeld("Deze regel is zojuist toegevoegd aan beeld")
    #~ ih.addRegelToProduct("Deze regel is zojuist toegevoegd aan product")
    #~ ih.addRegelToOmgeving("Deze regel is zojuist toegevoegd aan omgeving")
    #~ ih.wijzigBaten("Deze regel is zojuist toegevoegd aan de baten")
    #~ ih.wijzigKosten("Deze regel is zojuist toegevoegd aan de kosten")
    #~ printItem()
    #~ ih.wijzigRegelInKort("Deze regel is zojuist toegevoegd aan kort","Deze regel is zojuist gewijzigd aan kort")
    #~ ih.wijzigRegelInFunctie("Deze regel is zojuist toegevoegd aan functie","Deze regel is zojuist gewijzigd aan functie")
    #~ ih.wijzigRegelInBeeld("Deze regel is zojuist toegevoegd aan beeld","Deze regel is zojuist gewijzigd aan beeld")
    #~ ih.wijzigRegelInProduct("Deze regel is zojuist toegevoegd aan product","Deze regel is zojuist gewijzigd aan product")
    #~ ih.wijzigRegelInOmgeving("Deze regel is zojuist toegevoegd aan omgeving","Deze regel is zojuist gewijzigd aan omgeving")
    #~ ih.wijzigBaten("")
    #~ ih.wijzigKosten("")
    #~ printItem()
