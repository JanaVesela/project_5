import mysql.connector

def pripojeni():
    print("🔌 Zkouším se připojit...")
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="11111",
            database="spravce_ukolu",
            port=3306,
            connect_timeout=5,
            ssl_disabled=True,
            auth_plugin='mysql_native_password'
        )
        print("✅ Připojení úspěšné!")
        return conn
    except Exception as e:
        print("❌ Chyba při připojení:", e)


def vytvor_tabuku():
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("""
    CREATE TABLE IF NOT EXISTS ukoly (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nazev VARCHAR(100) NOT NULL,
        popis VARCHAR(100) NOT NULL,
        stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno'
    )
    """)

    conn.commit()

    kurzor.close()
    conn.close()

    print("Tabulka 'ukoly' byla vytvořena nebo už existuje.")

      
def pridat_ukol():
    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if nazev == "": #pokud uživatel nezadá název úkolu program vypíše chybovou hlášku a poté bude muset zadat znova název úkolu
            print("Název úkolu nesmí být prázdný.")
            continue
        popis = input("Zadejte popis úkolu: ").strip()
        if popis == "": #pokud uživatel nezadá popis úkolu program vypíše chybovou hlášku a poté bude muset zadat znova popis úkolu
            print("Popis úkolu nesmí být prázdný.")
            continue
        break

    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
    
    conn.commit()
    kurzor.close()
    conn.close()

    print("Úkol byl úspěšně přidán.")

def zobrazit_ukoly():
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("SELECT id, nazev FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')")
    vysledky = kurzor.fetchall()

    if not vysledky:
        print("Žádné úkoly nejsou k dispozici.")
    else:
        print("Seznam úkolů:")
        for ukol in vysledky:
            print(f"Název: {ukol[1]}")

    conn.commit()
    kurzor.close()
    conn.close()

def aktualizovat_ukol():
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("SELECT id, nazev, stav FROM ukoly")
    vysledky_1 = kurzor.fetchall()

    if not ukoly:
        print("Žádné úkoly nejsou dostupné")
        return

def odstranit_ukol():
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("SELECT id, nazev, FROM ukoly")
    ukoly = kurzor.fetchall()

    if not ukoly:
        print("Žádné úkoly nejsou k odstranění.")
        return
    while True:
        zobrazit_ukoly():
        
        cislo_ukolu = input("Zadejte číslo úkolu, který chcete odstranit: ").strip()
        if cislo_ukolu == "":
            print("Číslo úkolu nesmí být prázdné.")
            continue

        if not cislo_ukolu.isdigit():
            print("Zadejte platné číslo.")
            continue

        if cislo_ukolu < 0 or cislo_ukolu >= len(ukoly):
            print("Číslo úkolu neexistuje.")
            continue
        #potvrzeni a smazani
        ukol_k_odstraneni = 

        kurzor.execute("DELETE FROM ukoly WHERE id = %s")
        print("Úkol byl odstraněn.")

        kurzor.close()
        conn.close()

def hlavni_menu():
    vytvor_tabuku()
    while True:
        print("\n HLAVNÍ MENU")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyber možnost (1-5): ").strip()

        if volba == '1':
            pridat_ukol()
        elif volba == '2':
            zobrazit_ukoly()
        elif volba == '3':
            aktualizovat_ukol()
        elif volba == '4':
            odstranit_ukol()
        elif volba == '5':
            print("Program končí")
            break
        else:
            print("Neplatná volba, zadejte číslo mezi 1 a 5.")


if __name__ == "__main__":
    hlavni_menu()
