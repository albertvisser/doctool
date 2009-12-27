from xml.etree.ElementTree import ElementTree, Element, SubElement
from doctool_data_globals import *

class Relaties:
    "lijst alle gegevens van een bepaald item"
    def __init__(self,soort,item):
        self.fn = datapad + "relaties.xml" # naam van het xml bestand
        self.fno = datapad + "relaties.old" # naam van de backup van het xml bestand
        self.search_soort = soort
        self.search_item = item
        from os.path import exists
        self.exists = exists(self.fn)
        self.relvan = {}
        self.relnaar = {}

    def read(self):
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        for x in rt.findall("relatie"):
            vantype = x.get('vantype')
            van = x.get('van')
            naartype = x.get('naartype')
            naar = x.get('naar')
            if vantype == self.search_soort and van == self.search_item:
                if self.relnaar.has_key(naartype):
                    self.relnaar[naartype].append(naar)
                else:
                    self.relnaar[naartype] = [naar]
            if naartype == self.search_soort and naar == self.search_item:
                if self.relvan.has_key(vantype):
                    self.relvan[vantype].append(van)
                else:
                    self.relvan[vantype] = [van]

    def write(self,soort,item,remove=False):
        from shutil import copyfile
        copyfile(self.fn,self.fno)
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        if remove:
            for y in rt.findall("relatie"):
                vantype = y.get('vantype')
                van = y.get('van')
                naartype = y.get('naartype')
                naar = y.get('naar')
                if vantype == self.search_soort and van == self.search_item and naartype == soort and naar == item:
                    rt.remove(y)
        else:
            h = SubElement(rt,"relatie",vantype=self.search_soort,naartype=soort,van=self.search_item,naar=item)
        ElementTree(rt).write(self.fn)

    def addRelatie(self,soort,item):
        if self.relnaar.has_key(soort):
            self.relnaar[soort] = [item]
        else:
            self.relnaar[soort].append(item)
        self.write(soort,item)

    def remRelatie(self,soort,item):
        if self.relnaar.has_key(soort):
            try:
                self.relnaar[soort].remove(item)
            except:
                pass
            else:
                self.write(soort,item,remove=True)

    def wijzigRelatie(self,soort,item1,item2):
        self.remRelatie(soort,item1)
        self.addRelatie(soort,item2)

    def toonRelaties(self):
        for x in self.relnaar.keys():
            print ("relaties vanuit hier naar de volgende %ss:" % x)
            print "\t",
            for y in self.relnaar[x]:
                print y,
            print
        for x in self.relvan.keys():
            print ("relaties vanuit de volgende %ss naar hier:" % x)
            print "\t",
            for y in self.relvan[x]:
                print y,
            print


if __name__ == '__main__':
    s = Relaties("userspec","Zakgeld")
    s.read()
    s.toonRelaties()

    #~ soort = "funcproc"
    #~ item = "DocKies"
    #~ ih = Relaties(soort,item)
    #~ if ih.exists:
        #~ ih.read()
        #~ for x in ih.maakHtml():
            #~ print x
    #~ else:
        #~ print ("Nog geen relaties bij %s %s" % (soort,item))

    #~ ih.addRelatie(soort,"hallo")
    #~ ih.addRelatie(soort,"hello")
    #~ ih.addRelatie(soort,"arargh")
    #~ printItem()
    #~ ih.remRelatie(soort,"arargh")
    #~ printItem()
    #~ ih.wijzigRelatie(soort,"hello","hoi")
    #~ printItem()
    #~ ih.write()
