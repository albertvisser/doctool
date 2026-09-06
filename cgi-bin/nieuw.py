"""
hWat en hCat geven aan wat voor nieuw item het om gaat
naam en omschrijving zijn al opgegeven, als het goed is
  als vanuit een ander soort item wordt opgevoerd, worden hType en hName meegegeven
  hier moet een relatie naar gemaakt worden
"""
import shared
from main_logic.nieuw_main import nieuw

def main():
    form = shared.get_input()
    proj = form.getfirst("hProj", "")
    if not proj:
        proj = form.getfirst("hProj", "")
    wat = form.getfirst("hWat", "")
    catg = form.getfirst("hCat", "")
    naam = form.getfirst("txtNaam", "")
    oms = form.getfirst("txtOms", "")
    van_soort = form.getfirst("hType", "")
    van_naam = form.getfirst("hName", "")
    regels = nieuw(wat, catg, naam, oms, proj, van_soort, van_naam)
    shared.produce_output(regels)
    if len(regels) == 1:
        print()

if __name__ == '__main__':
   main()
