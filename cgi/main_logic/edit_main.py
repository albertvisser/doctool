import common
import docobj
from relaties import Relaties

fouthtml = "".join(common.fouthtml)

def edit_properties(docobject, proplist, form):
    if docobject.exists:
        dh.read()
    if isinstance(docobject, docobj.Project):
        h = form.get("txtNaam", None)
        if h is not None:
            dh.set_attr("naam", h)
    for ix, field in enumerate(proplist):
        h = form.get(field, None)
        if h is not None:
            docobject.set_attr(docobject.prpnames[ix], h)
    dh.write()

def edit_project(form):
    dh = docobj.Project(form.get("hProj"))
    edit_properties(dh, ("txtKort", "txtOms", "txtStart", "txtFysloc", "txtOpm"),
        form)

def edit_userspec(form):
    dh = docobj.Userspec(form.get("hWhich"))
    edit_properties(dh, ("txtKort", "txtFunc", "txtBeeld", "txtProduct", "txtBaten",
        "txtKosten", "txtOmg"), form)

def edit_userdocs(form):
    dh = docobj.UserDoc(form.get("hWhich"))
    edit_properties(dh, ("txtLink", "txtTekst"), form)

def edit_userwijz(form):
    dh = docobj.Userwijz(form.get("hWhich"))
    edit_properties(dh, ("txt", "txtOplos", "txtFuncA", "txtTechA", "txtRealA",
        "txtOpmerking"), form)

def edit_funcdocs(form):
    dh = docobj.FuncDoc(form.get("hWhich"))
    edit_properties(dh, ("txtLink", "txtTekst"), form)

def edit_functask(form):
    dh = docobj.Functask(form.get("hWhich"))
    edit_properties(dh, ("txtDoel", "txtWanneer", "txtWie", "txtWaarvoor",
        "txtCond", "txtBeschr"), form)

def edit_funcproc(form):
    dh = docobj.Funcproc(form.get("hWhich"))
    edit_properties(dh, ("txtDoel", "txtInvoer", "txtUitvoer", "txtWanneer",
        "txtWie", "txtWaarvoor", "txtCond", "txtBeschr"), form)

# funcdata (entiteit) (functie,opbouw,toegang,relatie,levensloop)>
def edit_techtask(form):
    dh = docobj.Techtask(form.get("hWhich"))
    edit_properties(dh, ("txtKort", "txtDoel", "txtPeriode", "txtVerloop"), form)

def edit_techproc(form):
    dh = docobj.Techproc(form.get("hWhich"))
    edit_properties(dh, ("txtTitel", "txtDoel", "txtInvoer", "txtUitvoer",
        "txtBeschr"), form)

# techdata gegevens (functie,opbouw,toegang,relatie,levensloop)>
def edit_procproc(form):
    dh = docobj.Procproc(form.get("hWhich"))
    edit_properties(dh, ("txtTitel", "txtDoel", "txtInvoer", "txtUitvoer",
        "txtWerkwijze", "txtBijzonder", "txtHoeTesten", "txtTestset"), form)

def edit_relaties(form):
    welk = form.get("hWhich", '')
    catg = form.get("hCat", '')
    wat = form.get("hWhat", '')
#-- ingevulde gegevens lezen
#-- list als er meer geselecteerd zijn, anders een string
    s_us = form.get("selUserspec", None)
    s_ft = form.get("selFunctask", None)
    s_fp = form.get("selFuncproc", None)
    ## s_fd = form.get("selFuncdata", None)
    s_tt = form.get("selTechtask", None)
    s_tp = form.get("selTechproc", None)
    ## s_td = form.get("selTechdata", None)
    s_pp = form.get("selProcproc", None)
    dh = Relaties(welk + catg, wat)
    # niet lezen, dan blijft alles leeg
    if isinstance(s_us, str):
        dh.add_relatie("userspec", s_us)
    elif s_us is not None:
        for x in s_us:
            dh.add_relatie("userspec", x)
    if isinstance(s_ft, str):
        dh.add_relatie("functask", s_ft)
    elif s_ft is not None:
        for x in s_ft:
            dh.add_relatie("funktask", x)
    if isinstance(s_fp, str):
        dh.add_relatie("funkproc", s_fp)
    elif s_fp is not None:
        for x in s_fp:
            dh.add_relatie("funkproc", x)
    if isinstance(s_tt, str):
        dh.add_relatie("techtask", s_tt)
    elif s_tt is not None:
        for x in s_tt:
            dh.add_relatie("techtask", x)
    if isinstance(s_tp, str):
        dh.add_relatie("techproc", s_tp)
    elif s_tp is not None:
        for x in s_tp:
            dh.add_relatie("techproc", x)
    #~ dh.write()

edit_func = {
    "project": edit_project,
    "userspec": edit_userspec,
    "userdocs": edit_userdocs,
    "userwijz": edit_userwijz,
    "funcdocs": edit_funcdocs,
    "functask": edit_functask,
    "funcproc": edit_funcproc,
    "funcdata": edit_funcdata,
    "techtask": edit_techtask,
    "techproc": edit_techproc,
    "techdata": edit_techdata,
    "procproc": edit_procproc,
    }

def edit(form):
    regels = []
    fout = False
    #-- argumenten lezen
    wat = form.get("hWhat", "")
    proj = form.get("hProj", "")
    cat = form.get("hCat", "")
    welk = form.get("hWhich", "")
    #-- fout melden (foutieve sturing)
    if wat == "" or proj == "" or (cat == "" and wat != "project") or \
            (welk == "" and wat != "project"):
        fout = True
        regels.append(fouthtml.format(wat, proj, cat, welk))
        return fout, regels
    #-- soort document bepalen
    h = wat + cat
    if h not in typcat:
        #-- fout melden bij niet bestaand soort document
        fout = True
        regels.append(common.soortfout_html.format(wat, cat))
        return fout, regels
    #-- item bijwerken: ingevulde gegevens lezen, deze omzetten in object en dit opslaan
    self.form = form
    regels = edit_func[h](form)
    if h != "project":
        edit_relaties(form)
    return fout, regels

if __name__ == '__main__':
	main()
#	test()
