import pytest
from src.spravce_ukolu import (
   pridat_ukol,
   zobrazit_ukoly,
   aktualizovat_ukol,
   odstranit_ukol,
   pripojeni
)

# Pomocná funkce pro vyčištění tabulky před testem
def vycisti_tabulku(conn):
    kurzor = conn.cursor()
    kurzor.execute("DELETE FROM ukoly")
    conn.commit()
    kurzor.close()


#pozitivni test pridání úkolu
def test_pridat_ukol_positive():
    conn = pripojeni()
    vycisti_tabulku(conn)

    # Přidáme úkol
    pridat_ukol("Nakup", "seznam_co_nakoupit", conn)
    
    # Ověříme, že úkol je v databázi
    ukol = zobrazit_ukoly(conn)
    nalezen = False
    for ukol in ukol:
        if ukol["nazev"] == "Nakup" and ukol["popis"] == "seznam_co_nakoupit":
            nalezen = True

    conn.close()
    assert nalezen == True


# Negativní test přidání úkolu (prázdný název)
def test_pridat_ukol_negative_nazev():
    conn = pripojeni()
    vycisti_tabulku(conn)

    with pytest.raises(ValueError):
        pridat_ukol("", "popis", conn)

    conn.close()


# Negativní test přidání úkolu (prázdný popis)
def test_pridat_ukol_negative_popis():
    conn = pripojeni()
    vycisti_tabulku(conn)

    with pytest.raises(ValueError):
        pridat_ukol("nazev", "", conn)

    conn.close()


#pozitivní test aktualizovat ukol
def test_aktualizovat_ukol_positive():
    conn = pripojeni()
    vycisti_tabulku(conn)

    pridat_ukol("Úklid", "uklidit pokoj", conn)
    ukoly = zobrazit_ukoly(conn)
    id_ukolu = ukoly[0]["id"]

    aktualizovat_ukol(id_ukolu, "hotovo", conn)
    ukoly = zobrazit_ukoly(conn)

    nalezen = False
    for ukol in ukoly:
        if ukol["id"] == id_ukolu and ukol["stav"] == "Hotovo":
            nalezen = True

    conn.close()
    assert nalezen == True


#negativní test aktualizovat ukol
#pokusíme se aktualizovat úkol který neexistuje
def test_aktualizovat_ukol_negative():
    conn = pripojeni()
    vycisti_tabulku(conn)

    with pytest.raises(ValueError):
        aktualizovat_ukol(98765, "Hotovo", conn)

    conn.close()


#pozitivní test odstranit úkol
def test_odstranit_ukol_positive():
    conn = pripojeni()
    vycisti_tabulku(conn)

    pridat_ukol("školka", "seznam úkolů školka", conn)
    ukoly = zobrazit_ukoly(conn)
    id_ukolu = ukoly[0]["id"]

    odstranit_ukol(id_ukolu, conn)
    ukoly = zobrazit_ukoly(conn)

    nalezen = any(ukol["id"] == id_ukolu for ukol in ukoly)

    conn.close()
    assert nalezen == False


#negativní test odstranit ukol
#pokusíme se odstranit úkol který neexistuje
def test_odstranit_ukol_negative():
    conn = pripojeni()
    vycisti_tabulku(conn)

    with pytest.raises(ValueError):
        odstranit_ukol(99999, conn)

    conn.close()