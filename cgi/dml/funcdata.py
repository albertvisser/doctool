from docitems import DocItem
from doctool_data_globals import datapad
xmlpad = datapad + "func_data/"

class Entiteit(DocItem):
    "lijst alle gegevens van een bepaald item"
    def __init__(self, naam,nieuw=False):
        DocItem.__init__(self,"entiteit",procnaam,nieuw)
        self.Naam = ""
        self.Functie = ""
        self.Attribuut = []
        self.Toegang = {}
        self.Relatie = {}
        self.Levensloop = []

    def nieuw(self):
        DocItem.nieuw(self,"entiteit")

    def read(self):
        DocItem.read(self)
        self.Naam = self.getPropText("naam")
        self.Functie = self.getPropText("functie")
        self.Attribuut = self.getAttribuut()
        self.Toegang = self.getToegang()
        self.Relatie = self.getRelaties()
        self.Levensloop = self.getPropList("levensloop")

    def getAttribuut(self):
        h = self.root.find("opbouw")
        if h is None:
            h = []
        else:
            hh = h.findall("attribuut")
            h = []
            for x in hh:
                i = [x.get("naam"),x.get("type")]
                t = x.find("omschrijving")
                if t is not None:
                    i.append(t.text)
                else:
                    i.append("")
                t = x.find("bijzonderheden")
                if t is not None:
                    i.append(t.text)
                else:
                    i.append("")
                h.append(i)
        return h

    def getToegang(self):
        h = {}
        for x in self.root.findall("toegang"):
            h[x.get("naam")] = x.get("volgorde")
        return h

    def getRelaties(self):
        h = {}
        for x in self.root.findall("relatie"):
            h[x.get("naam")] = x.get("entiteit")
        return h

    def write(self):
        self.getPropText("naam",self.Naam)
        self.getPropText("functie",self.Functie)
        self.getAttribuut(self.Attribuut)
        self.getToegang(self.Toegang)
        self.getRelaties(self.Relatie)
        self.getPropList("levensloop",self.Levensloop)
        DocItem.write(self)
        if not self.exists: self.exists = True

    def setAttribuut(self,h):
        o = self.root.find("opbouw")
        self.root.remove(o)
        s = SubElement(self.root,"opbouw")
        for x in h:
            ss = SubElement(s,"attribuut",naam=x[0],type=x[1])
            sss = SubElement(ss,"omschrijving")
            sss.text = x[2]
            sss = SubElement(ss,"bijzonderheden")
            sss.text = x[3]

    def setToegang(self,h):
        f = self.root.find("toegang")
        while h is not None:
            f.remove(h)
            f = self.root.find("toegang")
        for x in h.keys():
            s = SubElement(self.root,'toegang',naam=x,volgorde=h[x])

    def setRelaties(self,h):
        f = self.root.find("relatie")
        while h is not None:
            f.remove(h)
            f = self.root.find("relatie")
        for x in h.keys():
            s = SubElement(self.root,'relatie',naam=x,entiteit=h[x])

    def wijzigNaam(self,item):
        self.Naam = item

    def wijzigFunctie(self,item):
        self.Functie = item

    def addAttribuut(self,naam,type,oms,bijz):
        nieuw = 1
        for x in self.Attribuut:
            if x[0] == naam:
                nieuw = 0
                break
        if nieuw:
            item = [naam,type,oms,bijz]
            self.Attribuut.append(item)
            return 0
        else:
            return -1

    def wijzigAttribuut(self,naam,type,oms,bijz):
        gevonden = 0
        for x in self.Attribuut:
            if x[0] == naam:
                gevonden = 1
                break
        if gevonden:
            item = [naam,type,oms,bijz]
            i = self.Attribuut.index(item)
            self.Attribuut[i] = item
            return 0
        else:
            return -1

    def remAttribuut(self,naam):
        gevonden = 0
        for x in self.Attribuut:
            if x[0] == naam:
                gevonden = 1
                break
        if gevonden:
            self.Attribuut.remove(item)
            return 0
        else:
            return -1

    def addToToegang(self,naam,volgorde):
        if self.Toegang.has_key(naam):
            return -1
        else:
            self.Toegang[naam] = volgorde
            return 0

    def wijzigInToegang(self,naam,volgorde):
        if self.Toegang.has_key(naam):
            self.Toegang[naam] = volgorde
            return 0
        else:
            return -1

    def remFromToegang(self,naam):
        if self.Toegang.has_key(naam):
            del self.Toegang[naam]
            return 0
        else:
            return -1

    def addToRelatie(self,naam,entiteit):
        if self.Relatie.has_key(naam):
            return -1
        else:
            self.Relatie[naam] = entiteit
            return 0

    def wijzigInRelatie(self,naam,entiteit):
        if self.Relatie.has_key(naam):
            self.Relatie[naam] = entiteit
            return 0
        else:
            return -1

    def remFromRelatie(self,naam):
        if self.Relatie.has_key(naam):
            del self.Relatie[naam]
            return 0
        else:
            return -1

    def addRegelToLevensloop(self,item):
        self.Levensloop.append(item)

    def wijzigRegelInLevensloop(self,item,new):
        i = self.Levensloop.index(item)
        if new != item:
            self.Levensloop[i] = new

    def remRegelFromLevensloop(self,item):
        try:
            self.Levensloop.remove(item)
        except:
            pass

    def printItem(self,test):
        print ("====== object: %s ==========" % test)
        print "Naam: " + self.Naam
        print "Functie: " + self.Functie
        print "Attribuut: "
        for x in self.Attribuut:
            print (" %s, %s, %s, %s" % (x[0],x[1],x[2],x[3]))
        print "Toegang: "
        for x in self.Toegang.keys():
            print (" %s: %s" % (x,self.Toegang[x]))
        print "Relatie: "
        for x in self.Relatie.keys():
            print (" %s: %s" % (x,self.Relatie[x]))
        print "Levensloop: "
        for x in self.Levensloop:
            print " " + x

if __name__ == '__main__':
    from itemlist import ItemList
    lh = ItemList("funcdata")
    lh.read()
    test = lh.Items[0][1]
    ih = Entiteit(test)
    if ih.exists:
        ih.read()
        for x in ih.maakHtml():
            print x
    else:
        print test + " bestaat nog niet"
    #~ printItem(test,ih)
    #~ ih.wijzigNaam("Andere naam")
    #~ ih.wijzigFunctie("Andere functie")
    #~ h = "jaar"
    #~ if ih.addAttribuut(h,"tekst","x","y") == -1:
        #~ print ("Attribuut %s bestond al"% h)
    #~ if ih.addToToegang(h,"1") == -1:
        #~ print ("Toegang %s bestond al"% h)
    #~ h = "spaar"
    #~ if ih.addToRelatie(h,"1") == -1:
        #~ print ("Relatie %s bestond al"% h)
    #~ ih.addRegelToLevensloop("Deze regel is zojuist toegevoegd aan levensloop")
    #~ printItem(test,ih)
    #~ ih.write()
    #~ ih.wijzigNaam("Deze regel is zojuist gewijzigd aan Naam")
    #~ ih.wijzigRegelInAttribuut("Deze regel is zojuist toegevoegd aan attribuut","Deze regel is zojuist gewijzigd aan attribuut")
    #~ ih.wijzigRegelInToegang("Deze regel is zojuist toegevoegd aan toegang","Deze regel is zojuist gewijzigd aan toegang")
    #~ ih.wijzigRegelInLevensloop("Deze regel is zojuist toegevoegd aan levensloop","Deze regel is zojuist gewijzigd aan levensloop")
    #~ printItem(test,ih)