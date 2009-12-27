from doctool_globals import *
from types import *

class edit_main:
    def __init__(self,form):
        self.regels = []
        self.fout = False
        #-- argumenten lezen
        if form.has_key("hWhat"):
            wat = form["hWhat"]
        else:
            wat = ""
        if form.has_key("hProj"):
            proj = form["hProj"]
        else:
            proj = ""
        if form.has_key("hCat"):
            cat = form["hCat"]
        else:
            cat = ""
        if form.has_key("hWhich"):
            welk = form["hWhich"]
        else:
            welk = ""
        #-- fout melden (foutieve sturing)
        if wat == "" or proj == "" or (cat == "" and wat != "project") or (welk == "" and wat != "project"):
            self.fout = True
            self.regels.append("<html>")
            self.regels.append("<head></head>")
            self.regels.append("<body>")
            self.regels.append("Fout in aanroep: voor de juiste werking zijn tenminste vier argumenten nodig:<br />")
            self.regels.append("<br />")
            self.regels.append("hWhat: een hoofdcategorie (user, func, tech of proc)<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % wat)
            self.regels.append("<br />")
            self.regels.append("hProj: een projectnummer<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % proj)
            self.regels.append("<br />")
            self.regels.append("hCat: een subcategorie (user, func, tech of proc)<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % cat)
            self.regels.append("<br />")
            self.regels.append("hWhich: naam voor het te wijzigen item<br />")
            self.regels.append("     (de opgegeven waarde was: %s)<br />" % welk)
            self.regels.append("</body></html>")
            return
        #-- soort document bepalen
        try:
            h = wat + cat
            i = typcat.index(h)
        except ValueError:
            #-- fout melden bij niet bestaand soort document
            self.fout = True
            self.regels.append("<html>")
            self.regels.append("<head></head>")
            self.regels.append("<body>")
            self.regels.append("Fout in aanroep: je hebt een onjuiste combinatie van hoofd- en<br />")
            self.regels.append("  subcategorie opgegeven<br />")
            self.regels.append("     (de opgegeven waarde was: %s_%s)<br />" % (wat,cat))
            self.regels.append("</body></html>")
            return
        #-- item bijwerken: ingevulde gegevens lezen, deze omzetten in object en dit opslaan
        self.form = form
        if h == "project":
            self.edit_project()
        elif h == "userspec":
            self.edit_userspec()
        elif h == "userdocs":
            self.edit_userdocs()
        elif h == "userwijz":
            self.edit_userwijz()
        elif h == "funcdocs":
            self.edit_funcdocs()
        elif h == "functask":
            self.edit_functask()
        elif h == "funcproc":
            self.edit_funcproc()
        #~ elif h == "funcdata":
            #~ self.edit_funcdata()
        elif h == "techtask":
            self.edit_techtask()
        elif h == "techproc":
            self.edit_techproc()
        #~ elif h == "techdata":
            #~ self.edit_techdata()
        elif h == "procproc":
            self.edit_procproc()
        if h != "project":
            self.edit_relaties()

    def edit_project(self):
        from project import Project
        dh = Project(self.form["hProj"])
        if dh.exists: dh.read()
        if self.form.has_key("txtNaam"):
            dh.setAttr("naam",self.form["txtNaam"])
        if self.form.has_key("txtKort"):
            dh.setAttr("kort",self.form["txtKort"])
        if self.form.has_key("txtOms"):
            dh.setAttr("oms",self.form["txtOms"])
        if self.form.has_key("txtStart"):
            dh.setAttr("start",self.form["txtStart"])
        if self.form.has_key("txtFysloc"):
            dh.setAttr("fysloc",self.form["txtFysloc"])
        if self.form.has_key("txtOpm"):
            dh.setAttr("status",self.form["txtOpm"])
        dh.write()

    def edit_userspec(self):
        from userspec import Userspec
        dh = Userspec(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtKort"):
            dh.wijzigKort(self.form["txtKort"])
        if self.form.has_key("txtFunc"):
            for x in self.form["txtFunc"].split("\n"):
                dh.addRegelToFunctie(x[:-1])
        if self.form.has_key("txtBeeld"):
            for x in self.form["txtBeeld"].split("\n"):
                dh.addRegelToBeeld(x[:-1])
        if self.form.has_key("txtProduct"):
            for x in self.form["txtProduct"].split("\n"):
                dh.addRegelToProduct(x[:-1])
        if self.form.has_key("txtBaten"):
            dh.wijzigBaten(self.form["txtBaten"])
        if self.form.has_key("txtKosten"):
            dh.wijzigKosten(self.form["txtKosten"])
        if self.form.has_key("txtOmg"):
            for x in self.form["txtOmg"].split("\n"):
                dh.addRegelToOmgeving(x[:-1])
        dh.write()

    def edit_userdocs(self):
        from userdocs import UserDoc
        dh = UserDoc(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtLink"):
            dh.wijzigLink(self.form["txtLink"])
        if self.form.has_key("txtTekst"):
            dh.wijzigTekst(self.form["txtTekst"].split("\n"))
        dh.write()

    def edit_userwijz(self):
        from userwijz import Userwijz
        dh = Userwijz(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtWens"):
            dh.wijzigWens(self.form["txt"])
        if self.form.has_key("txtOplos"):
            dh.addRegelToOplossing(self.form["txtOplos"])
        if self.form.has_key("txtFuncA"):
            dh.addRegelToFuncAanv(self.form["txtFuncA"])
        if self.form.has_key("txtTechA"):
            dh.addRegelToTechAanv(self.form["txtTechA"])
        if self.form.has_key("txtRealA"):
            dh.addRegelToRealisatie(self.form["txtRealA"])
        if self.form.has_key("txtOpmerking"):
            dh.addRegelToOpmerkingen(self.form["txtOpmerking"])
        dh.write()

    def edit_funcdocs(self):
        from funcdocs import FuncDoc
        dh = FuncDoc(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtTekst"):
            dh.wijzigTekst(self.form["txtTekst"].split("\n"))
        dh.write()

    # functask (gebrtaak)  (doel,wanneer,wie,waarvoor,condities,beschrijving)>
    def edit_functask(self):
        from functask import Functask
        dh = Functask(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtDoel"):
            dh.wijzigDoel(self.form["txtDoel"])
        if self.form.has_key("txtWanneer"):
            for x in self.form["txtWanneer"].split("\n"):
                dh.addRegelToWanneer(x[:-1])
        if self.form.has_key("txtWie"):
            for x in self.form["txtWie"].split("\n"):
                dh.addRegelToWie(x[:-1])
        if self.form.has_key("txtWaarvoor"):
            for x in self.form["txtWaarvoor"].split("\n"):
                dh.addRegelToWaarvoor(x[:-1])
        if self.form.has_key("txtCond"):
            for x in self.form["txtCond"].split("\n"):
                dh.addRegelToCondities(x[:-1])
        if self.form.has_key("txtBeschr"):
            for x in self.form["txtBeschr"].split("\n"):
                dh.addRegelToBeschrijving(x[:-1])
        dh.write()

    # funcproc (doel,invoer,uitvoer,beschrijving)>
    def edit_funcproc(self):
        from funcproc import Funcproc
        dh = Funcproc(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtDoel"):
            dh.wijzigDoel(self.form["txtDoel"])
        if self.form.has_key("txtInvoer"):
            for x in self.form["txtInvoer"].split("\n"):
                dh.addRegelToInvoer(x[:-1])
        if self.form.has_key("txtUitvoer"):
            for x in self.form["txtUitvoer"].split("\n"):
                dh.addRegelToUitvoer(x[:-1])
        if self.form.has_key("txtBeschr"):
            for x in self.form["txtBeschr"].split("\n"):
                dh.addRegelToBeschrijving(x[:-1])
        dh.write()

    # funcdata (entiteit) (functie,opbouw,toegang,relatie,levensloop)>

    # techtask (kort,doel,periode,verloop)>
    def edit_techtask(self):
        from techtask import Techtask
        dh = Techtask(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtKort"):
            dh.wijzigKort(self.form["txtKort"])
        if self.form.has_key("txtDoel"):
            dh.wijzigDoel(self.form["txtDoel"])
        if self.form.has_key("txtPeriode"):
            for x in self.form["txtPeriode"].split("\n"):
                dh.addRegelToPeriode(x[:-1])
        if self.form.has_key("txtVerloop"):
            for x in self.form["txtVerloop"].split("\n"):
                dh.addRegelToVerloop(x[:-1])
        dh.write()

    # techproc (titel,doel,invoer,uitvoer,beschrijving)>
    def edit_techproc(self):
        from techproc import Techproc
        dh = Techproc(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtTitel"):
            dh.wijzigTitel(self.form["txtTitel"])
        if self.form.has_key("txtDoel"):
            dh.wijzigDoel(self.form["txtDoel"])
        if self.form.has_key("txtInvoer"):
            for x in self.form["txtInvoer"].split("\n"):
                dh.addRegelToInvoer(x[:-1])
        if self.form.has_key("txtUitvoer"):
            for x in self.form["txtUitvoer"].split("\n"):
                dh.addRegelToUitvoer(x[:-1])
        if self.form.has_key("txtBeschr"):
            for x in self.form["txtBeschr"].split("\n"):
                dh.addRegelToBeschrijving(x[:-1])
        dh.write()

    # techdata gegevens (functie,opbouw,toegang,relatie,levensloop)>

    # procproc procedure (titel,doel,invoer,uitvoer,werkwijze,bijzonder,hoetetesten,testgevallen)>
    def edit_procproc(self):
        from procproc import Procproc
        dh = Procproc(self.form["hWhich"])
        if dh.exists: dh.read()
        if self.form.has_key("txtTitel"):
            dh.wijzigTitel(self.form["txtTitel"])
        if self.form.has_key("txtDoel"):
            dh.wijzigDoel(self.form["txtDoel"])
        if self.form.has_key("txtInvoer"):
            for x in self.form["txtInvoer"].split("\n"):
                dh.addRegelToInvoer(x[:-1])
        if self.form.has_key("txtUitvoer"):
            for x in self.form["txtUitvoer"].split("\n"):
                dh.addRegelToUitvoer(x[:-1])
        if self.form.has_key("txtWerkwijze"):
            for x in self.form["txtWerkwijze"].split("\n"):
                dh.addRegelToWerkwijze(x[:-1])
        if self.form.has_key("txtBijzonder"):
            for x in self.form["txtBijzonder"].split("\n"):
                dh.addRegelToBijzonder(x[:-1])
        if self.form.has_key("txtHoeTesten"):
            for x in self.form["txtHoeTesten"].split("\n"):
                dh.addRegelToHoetetesten(x[:-1])
        if self.form.has_key("txtTestset"):
            for x in self.form["txtTestset"].split("\n"):
                dh.addRegelToTestgevallen(x[:-1])
        dh.write()

    def edit_relaties(self):
        welk = self.form["hWhich"]
        catg = self.form["hCat"]
        wat = self.form["hWhat"]
        s_us = None
        s_ft = None
        s_fp = None
        s_fd = None
        s_tt = None
        s_tp = None
        s_td = None
        s_pp = None
    #-- ingevulde gegevens lezen
    #-- list als er meer geselecteerd zijn, anders een string
        if self.form.has_key("selUserspec"):
            s_us = self.form["selUserspec"]
        if self.form.has_key("selFunctask"):
            s_ft = self.form["selFunctask"]
        if self.form.has_key("selFuncproc"):
            s_fp = self.form["selFuncproc"]
        #~ if self.form.has_key("selFuncdata"):
            #~ s_fd = self.form["selFuncdata"]
        if self.form.has_key("selTechtask"):
            s_tt = self.form["selTechtask"]
        if self.form.has_key("selTechproc"):
            s_tp = self.form["selTechproc"]
        #~ if self.form.has_key("selTechdata"):
            #~ s_td = self.form["selTechdata"]
        #~ if self.form.has_key("selProcproc"):
            #~ s_pp = self.form["selProcproc"]
        from relaties import Relaties
        dh = Relaties(welk+catg,wat)
        # niet lezen, dan blijft alles leeg
        if type(s_us) == StringType:
            dh.addRelatie("userspec",s_us)
        elif type(s_us) == ListType:
            for x in s_us:
                dh.addRelatie("userspec",x)
        if type(s_ft) == StringType:
            dh.addRelatie("functask",s_ft)
        elif type(s_ft) == ListType:
            for x in s_ft:
                dh.addRelatie("funktask",x)
        if type(s_fp) == StringType:
            dh.addRelatie("funkproc",s_fp)
        elif type(s_fp) == ListType:
            for x in s_fp:
                dh.addRelatie("funkproc",x)
        if type(s_tt) == StringType:
            dh.addRelatie("techtask",s_tt)
        elif type(s_tt) == ListType:
            for x in s_tt:
                dh.addRelatie("techtask",x)
        if type(s_tp) == StringType:
            dh.addRelatie("techproc",s_tp)
        elif type(s_tp) == ListType:
            for x in s_tp:
                dh.addRelatie("techproc",x)
        #~ dh.write()

if __name__ == '__main__':
	main()
#	test()
