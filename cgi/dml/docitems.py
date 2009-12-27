#! C:/python23
# -*- coding: UTF-8 -*-

from xml.etree.ElementTree import ElementTree, Element, SubElement
from doctool_data_globals import datapad
#~ datapad = "Z:/pythoneer/doctool/data/"


class DataError(Exception):
    pass

class LaatsteWijz:
    def __init__(self,jaar=None):
        if jaar == None:
            from datetime import date
            jaar = str(date.today().year)
        tree = ElementTree(file=datapad + "user_wijz.xml")
        nummer = 0
        rt = tree.getroot()
        for x in rt.findall("item"):
            t = x.get("titel").split("-")
            if t[0] != jaar: continue
            if int(t[1]) > nummer: nummer = int(t[1])
        self.nieuwnummer = nummer + 1
        self.nieuwetitel = ("%s-%04i" % (jaar,self.nieuwnummer))

class ItemList:
    "lijst alle items van een bepaald soort"
    def __init__(self,cat,sel="0",force=False):
        self.cat = cat
        self.sel = sel
        if cat == "project":
            s = cat
        else:
            s = "_".join((cat[:4],cat[4:]))
        self.fn = datapad + s + ".xml" # naam van het xml bestand
        self.fno = datapad + s + ".old" # naam van de backup van het xml bestand
        self.Items = []
        from os.path import exists
        self.exists = exists(self.fn)
        #~ print "self.fn was",self.fn,self.exists
        if self.exists:
            self.read()
        else:
            if force:
                fh = open(self.fn,"w")
                fh.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
                if cat == "project":
                    fh.write('<projecten>\n')
                    fh.write('</projecten>\n')
                else:
                    fh.write('<lijst>\n')
                    fh.write('</lijst>\n')
                fh.close()

    def read(self):
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        if self.cat == "project":
            for x in rt.findall("project"):
                proj  = x.get("id")
                naam = x.get("naam")
                oms = x.find("kort").text
                self.Items.append((proj,naam,oms))
        else:
            for x in rt.findall("item"):
                proj = x.get("project")
                naam = x.get("titel")
                oms = x.text
                if self.sel == "0":
                    self.Items.append((proj,naam,oms))
                elif proj == self.sel:
                    self.Items.append((naam,oms))
        self.aantItems = len(self.Items)

    def write(self):
        if self.cat == "project": # in dat geval via project.py bijwerken
            return False
        if self.sel != "0":
            return False
        from shutil import copyfile
        copyfile(self.fn,self.fno)
        rt = Element("lijst")
        for x in self.Items:
            h = SubElement(rt,"item",project=x[0],titel=x[1])
            h.text = x[2]
        ElementTree(rt).write(self.fn)

    def addListItem(self,titel,oms,proj="0"):
        if self.cat == "project": # toevoegen gaat via project.py
            self.fout = "project toevoegen gaat niet op deze manier"
            return False
        ok = True
        self.fout = ""
        for x in enumerate(self.Items):
            if x[1][1] == titel:
                self.fout = "item bestaat al"
                ok = False
                break
        if ok:
            if proj == "0" or proj == "":
                # iets moet altijd aan een bepaald project toegekend zijn
                self.fout = "item moet wel bij een project horen"
                ok = False
            #~ elif type(proj) is list: - voor als een AW over projecten heen mag gaan
                #~ if self.cat == "userwijz":
                # wijzigingen kunnen meer projecten raken?
                    #~ pass
                #~ else:
                    #~ self.fout = "item mag maar bij één project horen"
                    #~ ok = False
        if ok:
            self.Items.append((proj,titel,oms))
            self.aantItems = len(self.Items)
        return ok

    def remListItem(self,titel):
        ok = False
        self.fout = "Item niet gevonden"
        # we gaan ervan uit dat controles zoals zijn er nog relaties met dit
        # item en hangen er nog zaken bij dit project elders gedaan zijn
        for x in enumerate(self.Items):
            if x[1][1] == titel:
                self.Items.remove(self.Items[x[0]])
                self.aantItems = len(self.Items)
                ok = True
                self.fout = ""
                break
        return ok

    def editListItem(self,titel,oms):
        ok = False
        self.fout = "Item niet gevonden"
        for x in enumerate(self.Items):
            if x[1][1] == titel:
                h = x[1]
                self.Items[x[0]] = (h[0],h[1],oms)
                ok = True
                self.fout = ""
                break
        return ok

class DocItem:
    "lijst alle gegevens van een bepaald item"
    def __init__(self,cat,procnaam,nieuwitem=False):
        xmlpad = datapad + "_".join((cat[:4],cat[4:])) + "/"
        self.fn = xmlpad + procnaam + ".xml" # naam van het xml bestand
        self.fno = xmlpad + procnaam + ".old" # naam van de backup van het xml bestand
        self.exists = False
        from os.path import exists
        if exists(self.fn):
            self.exists = True
            #~ self.read()
        elif nieuwitem:
            self.nieuw()

    def nieuw(self,naam):
        f = file(self.fn,"w")
        f.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
        f.write('<%s>\n' % naam)
        f.write('</%s>\n' % naam)
        f.close()
        self.root = Element(naam)

    def read(self):
        tree = ElementTree(file=self.fn)
        self.root = tree.getroot()

    def getPropList(self,naam):
        h = self.root.find(naam)
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

    def getPropAttr(self,naam):
        h = self.root.get(naam)
        if h is None:
            h = ""
        return h

    def getPropText(self,naam):
        h = self.root.find(naam)
        if h is None:
            h = ""
        else:
            hh = h.text
            if hh is None:
                h = ""
            else:
                h = hh
        return h

    def getSubPropText(self,naam,pad):
        h = self.root.find(pad)
        if h is None:
            h = ""
        else:
            hh = h.find(naam)
            if hh is None:
                h = ""
            else:
                h = hh.text
                if h is None: h = ""
        return h

    def write(self):
        tree = ElementTree(self.root)
        tree.write(self.fn)
        self.exists = True

    def setPropList(self,name,value):
        h = self.root.find(name)
        if h is None:
            h = SubElement(self.root,name)
        else:
            hh = h.find("regel")
            while hh is not None:
                h.remove(hh)
                hh = h.find("regel")
        for x in value:
            hh = SubElement(h,"regel")
            hh.text = x

    def setPropText(self,name,value):
        h = self.root.find(name)
        if h is None:
            h = SubElement(self.root,name)
        h.text = value

    def setSubPropText(self,name,pad,value):
        h = self.root.find(pad)
        if h is None:
            h = SubElement(self.root,pad)
        hh = h.find(name)
        if hh is None:
            hh = SubElement(h,name)
        hh.text = value

    def setPropAttr(self,name,attr,value):
        h = self.root.find(name)
        if h is None:
            h = SubElement(self.root,name)
        h.set(attr,value)


def test_ItemList():
    h = LaatsteWijz()
    print h.nieuwetitel
    print "#---- na inlezen ---#"
    h = ItemList("userspec")
    for x in h.Items:
        print x
    if not h.addListItem("ahum","keelgeschraap"):
        print h.fout
    else:
        h.write()
    h.read()
    print "#---- na toevoegen ---#"
    for x in h.Items:
        print x
    if not h.editListItem("ahum","gargelbork"):
        print h.fout
    else:
        h.write()
    h.read()
    print "#---- na wijzigen ---#"
    for x in h.Items:
        print x
    if not h.remListItem("ahum"):
        print h.fout
    else:
        h.write()
    h.read()
    print "#---- na verwijderen ---#"
    for x in h.Items:
        print x



if __name__ == "__main__":
    test_ItemList()