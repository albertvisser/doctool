# -*- coding: UTF-8 -*-

"""Deze module bevat een aantal algemene classes bruikbaar als base classes voor
diverse documenten, alsmede functies om de laatst uitgegeven/eerstvolgend uit te
geven volgnummers te bepalen"""

import os
import shutil
from datetime import date
from xml.etree.ElementTree import ElementTree, Element, SubElement
from doctool_data_common import datapad

class DataError(Exception):
    pass

def laatste_proj():
    "functie om het nieuw te gebruiken projectnummer te bepalen"
    tree = ElementTree(file=os.path.join(datapad, "project.xml"))
    rt = tree.getroot()
    i = 0
    for x in rt.findall("project"):
        h = int(x.get("id"))
        if h > i:
            i = h
    return str(i + 1)

def laatste_wijz(zoekjaar=None):
    """bepaal voor een userwijz het te gebruiken volgnummer

    kan met een jaar worden aangestuurd om het nummer voor dat jaar te bepalen
    bij ontbreken van een jaar wordt het huidige gebruikt"""
    if zoekjaar is None:
        zoekjaar = str(date.today().year)
    tree = ElementTree(file=os.path.join(datapad, "user_wijz.xml"))
    nummer = 0
    rt = tree.getroot()
    for x in rt.findall("item"):
        jaar, volgnr = x.get("titel").split("-")
        if jaar == jaar and int(volgnr) > nummer:
            nummer = int(volgnr)
    nieuwnummer = nummer + 1
    nieuwetitel = "%s-%04i" % (jaar, nieuwnummer)
    return nieuwnummer, nieuwetitel

class ItemList(object):
    "lijst alle items van een bepaald soort"
    def __init__(self, cat, sel="0", force=False):
        """leest de lijst van het opgegeven soort.
        Maakt een nieuwe lijst aan indien die nog niet bestaat"""
        self.cat = cat
        self.sel = sel
        if cat == "project":
            s = cat
        else:
            s = "_".join((cat[:4], cat[4:]))
        self.fn = os.path.join(datapad, s + ".xml") # naam van het xml bestand
        self.fno = os.path.join(datapad, s + ".old") # naam van de backup van het xml bestand
        self.items = []
        self.exists = os.path.exists(self.fn)
        #~ print "self.fn was",self.fn,self.exists
        if self.exists:
            self.read()
        elif force:
            with open(self.fn,"w") as fh:
                fh.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
                if cat == "project":
                    fh.write('<projecten>\n')
                    fh.write('</projecten>\n')
                else:
                    fh.write('<lijst>\n')
                    fh.write('</lijst>\n')
            self.exists = True
        self.aant_items = len(self.items)

    def read(self):
        "stelt de lijst samen op basis van een xml bestand"
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        self.items = []
        if self.cat == "_project":
            for x in rt.findall("project"):
                proj  = x.get("id")
                naam = x.get("naam")
                oms = x.find("kort").text
                self.items.append((proj,naam,oms))
        else:
            for x in rt.findall("item"):
                proj = x.get("project")
                naam = x.get("titel")
                oms = x.text
                if self.sel == "0":
                    self.items.append((proj, naam, oms))
                elif proj == self.sel:
                    self.items.append((naam, oms))

    def write(self):
        "schrijft de aangepaste lijst terug als xml-bestand"
        if self.sel != "0":
            return False
        shutil.copyfile(self.fn, self.fno)
        if self.cat == "project": # in dat geval via project.py bijwerken
            rt = Element("projecten")
        else:
            rt = Element("lijst")
        for proj, titel, oms in self.items:
            h = SubElement(rt, "item", project=proj, titel=titel)
            h.text = oms
        ElementTree(rt).write(self.fn)

    def add_listitem(self, titel, oms, proj="0"):
        "voegt een item toe aan de lijst"
        ## if self.cat == "project": # toevoegen gaat via project.py
            ## self.fout = "project toevoegen gaat niet op deze manier"
            ## return False
        ok = True
        self.fout = ""
        for item in self.items:
            if item[1] == titel:
                self.fout = "item bestaat al"
                ok = False
                break
        if ok and proj in ("0", ""):
            self.fout = "item moet wel bij een project horen"
            ok = False
        if ok:
            self.items.append((proj, titel, oms))
            self.aant_items = len(self.items)
        return ok

    def rem_listitem(self, titel):
        "verwijder een item uit de lijst"
        ok = False
        self.fout = "Item niet gevonden"
        # we gaan ervan uit dat controles zoals zijn er nog relaties met dit
        # item en hangen er nog zaken bij dit project elders gedaan zijn
        for item in self.items:
            if item[1] == titel:
                self.items.remove(item)
                self.aant_items = len(self.items)
                ok = True
                self.fout = ""
                break
        return ok

    def edit_listitem(self, titel, oms):
        "wijzig een item in de lijst"
        ok = False
        self.fout = "Item niet gevonden"
        for idx, item in enumerate(self.items):
            if item[1] == titel:
                self.items[idx] = item[0],item[1],oms
                ok = True
                self.fout = ""
                break
        return ok

class DocItem(object):
    "base class voor het weergeven van een document van een bepaald type"
    def __init__(self, cat, procnaam, nieuwitem=False):
        "initialisatie; maakt indien gewenst een nieuw leeg item aan"
        self.prpnames = {
            "single": {'type': "text", },
            "multi": {'type': "list", },
            }
        self._cat = cat
        if cat == "project":
            # eerst de projecten index lezen om een nummer om te zetten in een naam
            tree = ElementTree(file=os.path.join(datapad, 'project.xml'))
            root = tree.getroot()
            for x in root.findall('item'):
                if x.get('project') == procnaam:
                    procnaam = x.get('titel')
                    self.naam = x.text
                    break
            xmlpad = os.path.join(datapad, cat)
            self._fn = os.path.join(xmlpad, procnaam + ".xml")
        else:
            xmlpad = os.path.join(datapad, "{}_{}".format(cat[:4],cat[4:]))
            self._fn = os.path.join(xmlpad, procnaam.lower() + ".xml")
        self._procnaam = procnaam
        self._fno = os.path.splitext(self._fn)[0] + ".old"
        self.exists = os.path.exists(self._fn)
        if not self.exists and nieuwitem:
            self.nieuw()

    def __str__(self):
        return '{} "{}" '.format(self._cat, self._procnaam)

    def print_item(self):
        "standaard weergave van de document onderdelen"
        print str(self), "bestaat: ", self.exists
        for prop in self.prpnames:
            h = self.__getattribute__(prop)
            print prop + ": ",
            if self.prpnames[prop]['type'] == 'list':
                if len(h) > 0:
                    print
                    for x in h:
                        print x
                else:
                    print "(leeg)"
            else:
                print h
        print

    def nieuw(self):
        """maak een nieuwe documentweergave aan
        de gedefinieerde attributen worden leeg geinitialiseerd"""
        ## with open(self._fn, "w") as f:
            ## f.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
            ## f.write('<%s>\n' % self._procnaam)
            ## f.write('</%s>\n' % self._procnaam)
        self._root = Element(self._procnaam)
        for prop in self.prpnames:
            if self.prpnames[prop]['type'] in ("text", "attr"):
                self.__setattr__(prop, "")
            elif self.prpnames[prop]['type'] == 'list':
                self.__setattr__(prop, [])

    def read(self):
        """zet een xml document om in een interne weergave"""
        tree = ElementTree(file=self._fn)
        self._root = tree.getroot()
        for prop in self.prpnames:
            self.__setattr__(prop, DocItem.get_attr(self, prop))

    def write(self):
        """schrijf de interne weergave weg als een xml document.
        de eerdere versie wordt niet gebackupd!?"""
        for prop in self.prpnames:
            elem = SubElement(self._root, prop)
            data = self.__getattribute__(prop)
            if self.prpnames[prop]['type'] == "text":
                elem.text = data
            elif self.prpnames[prop]['type'] == 'list':
                for x in data:
                    SubElement(elem, 'regel').text = x
            elif self.prpnames[prop]['type'] == 'attr':
                elem.set(self.prpnames[prop]['naam'], data)
        tree = ElementTree(self._root)
        tree.write(self._fn)
        if not self.exists:
            self.exists = True

    def get_proplist(self, naam):
        """lees een attribuut dat gedefineerd is als 'list' element
        het wordt verondersteld samengesteld te zijn uit 'regel' subelementen"""
        h = self._root.find(naam)
        if h is None:
            h = []
        else:
            hh = h.findall("regel")
            h = []
            for x in hh:
                if x.text is None:
                    h.append("")
                else:
                    h.append(x.text.rstrip())
        return h

    def get_propattr(self, naam, attr):
        """lees een attribuut dat gedefinieerd is als 'attribuut' van een element
        de naam van het betreffende attribuut moet ook meegegeven worden"""
        h = self._root.find(naam)
        if h is None:
            h = ""
        else:
            hh = h.get(attr)
            if hh is None:
                h = ""
            else:
                h = hh
        return h

    def get_proptext(self, naam):
        """lees een attribuut dat gedefinieerd is als 'text' bij een element
        """
        h = self._root.find(naam)
        if h is None:
            h = ""
        else:
            hh = h.text
            if hh is None:
                h = ""
            else:
                h = hh
        return h

    def get_subproptext(self, naam, pad):
        """lees een attribuut dat gedefinieerd is als tekst bij een 'subelement'
        het pad (subelement) moet hierbij ook opgegeven worden"""
        h = self._root.find(pad)
        if h is None:
            h = ""
        else:
            hh = h.find(naam)
            if hh is None:
                h = ""
            else:
                h = hh.text
                if h is None:
                    h = ""
        return h

    def get_attr(self, naam):
        "stel het aangegeven attribuut in vanuit de xml"
        if self.prpnames[naam]['type'] == "text":
            return self.get_proptext(naam)
        elif self.prpnames[naam]['type'] == "attr":
            return self.get_propattr(naam, self.prpnames[naam]['naam'])
        elif self.prpnames[naam]['type'] == 'list':
            return self.get_proplist(naam)
        elif self.prpnames[naam]['type'] == 'prop':
            return self.get_subproptext(naam, self.prpnames[naam]['pad'])

    def set_proplist(self, name, value):
        h = self._root.find(name)
        if h is None:
            h = SubElement(self._root, name)
        else:
            hh = h.find("regel")
            while hh is not None:
                h.remove(hh)
                hh = h.find("regel")
        for x in value:
            hh = SubElement(h,"regel")
            hh.text = x

    def set_proptext(self, name, value):
        h = self._root.find(name)
        if h is None:
            h = SubElement(self._root, name)
        h.text = value

    def set_subproptext(self, name, pad, value):
        h = self._root.find(pad)
        if h is None:
            h = SubElement(self._root, pad)
        hh = h.find(name)
        if hh is None:
            hh = SubElement(h, name)
        hh.text = value

    def set_propattr(self, name, attr, value):
        h = self._root.find(name)
        if h is None:
            h = SubElement(self._root, name)
        h.set(attr, value)

    def set_attr(self, naam, waarde):
        "stel het aangegeven attribuut in de xml in"
        if self.prpnames[naam]['type'] == "text":
            self.set_proptext(naam, waarde)
        elif self.prpnames[naam]['type'] == 'list':
            self.set_proplist(naam, waarde)
        elif self.prpnames[naam]['type'] == 'attr':
            self.set_propattr(naam, self.prpnames[naam]['naam'], waarde)
