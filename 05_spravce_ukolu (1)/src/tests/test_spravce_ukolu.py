import pytest
from src.spravce_ukolu import (
   pridat_ukol,
   zobrazit_ukoly,
   aktualizovat_ukol,
   odstranit_ukol
)

#pozitivni test pridání úkolu
def test_pridat_ukol_positive():
    # Přidáme úkol
    pridat_ukol("Nakup", "seznam_co_nakoupit")
    
    # Ověříme, že úkol je v databázi
    ukol = zobrazit_ukoly()
    nalezen = False
    for ukol in ukol:
        if ukol["nazev"] == "Nakup" and ukol["popis"] == "seznam_co_nakoupit":
            nalezen = True

    assert nalezen == True

# Negativní test přidání úkolu (prázdný název)
def test_pridat_ukol_negative_nazev():
    with pytest.raises(ValueError):
        pridat_ukol("", "popis")

# Negativní test přidání úkolu (prázdný popis)
def test_pridat_ukol_negative_popis():
    with pytest.raises(ValueError):
        pridat_ukol("nazev", "")

#pozitivní test aktualizovat ukol
def test_aktualizovat_ukol_positive():
    aktualizovat_ukol(1, "Hotovo")
    ukoly = zobrazit_ukoly()
    nalezen = False
    for ukol in ukoly:
        if ukol["id"] == 1 and ukol["stav"] == "Hotovo":
            nalezen = True

    assert nalezen == True

#negativní test aktualizovat ukol
#pokusíme se aktualizovat úkol který neexistuje
def test_aktualizovat_ukol_negative():
    with pytest.raises(ValueError):
        aktualizovat_ukol(98765, "Hotovo")

#pozitivní test odstranit úkol
def test_odstranit_ukol_positive():
    #pridame ukol co pak odstranime
    pridat_ukol("školka","seznam úkolů školka")

    ukoly = zobrazit_ukoly()
    id_ukolu = None
    for ukol in ukoly:
        if ukol["nazev"] == "školka":
            id_ukolu = ukol["id"]
            break

    odstranit_ukol(id_ukolu)

    ukoly = zobrazit_ukoly()
    nalezen = False
    for ukol in ukoly:
        if ukol["id"] == id_ukolu:
            nalezen = True

    assert nalezen == False


#negativní test odstranit ukol
#pokusíme se odstranit úkol který neexistuje
def test_odstranit_ukol_negative():
    with pytest.raises(ValueError):
        odstranit_ukol(98765)