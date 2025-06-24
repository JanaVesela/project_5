import mysql.connector

def pripojeni():
    print("🔌 Připojuji se ...")
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="11111",
            database="spravce_ukolu",
            port=3306,
            connect_timeout=5,
            ssl_disabled=True
        )
        print("✅ Připojení úspěšné!")
        return conn
    except Exception as e:
        print("❌ Chyba při připojení:", e)
        exit()


def vytvor_databazi():
    """Vytvoří databázi, pokud neexistuje."""
    conn = pripojeni()
    kurzor = conn.cursor()
    kurzor.execute("CREATE DATABASE IF NOT EXISTS spravce_ukolu")
    conn.commit()
    kurzor.close()
    conn.close()
    print("✅ Databáze 'spravce_ukolu' je připravena.")


def vytvor_tabulku(conn):
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

    print("Tabulka 'ukoly' je připravena.")


def pridat_ukol(nazev, popis, conn):
    if not nazev.strip():
        raise ValueError("Název úkolu nesmí být prázdný.")
    if not popis.strip():
        raise ValueError("Popis úkolu nesmí být prázdný.")
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ukoly (nazev, popis)
        VALUES (%s, %s)
    """, (nazev, popis))
    conn.commit()
    cursor.close()
    print("✅ Úkol přidán.")

def zobrazit_ukoly(conn):
    kurzor = conn.cursor()

    kurzor.execute("SELECT id, nazev, popis, stav FROM ukoly")
    vysledky = kurzor.fetchall()

    kurzor.close()

    if not vysledky:
        print(" Žádné úkoly zatím nejsou.")
    else:
        print("\n Seznam úkolů:")
        for id, nazev, popis, stav in vysledky:
            print(f"ID: {id} | Název: {nazev} | Popis: {popis} | Stav: {stav}")

def ukol_existuje(id_ukolu, conn):
    kurzor = conn.cursor()
    kurzor.execute("SELECT 1 FROM ukoly WHERE id = %s", (id_ukolu,))
    exists = kurzor.fetchone() is not None
    kurzor.close()
    return exists


def aktualizovat_ukol(id_ukolu, novy_stav, conn):
    stav = {
        'probíhá' : 'Probíhá',
        'hotovo' : 'Hotovo'
    }

    if novy_stav not in stav:
        raise ValueError("Neplatný stav. Zadejte 'Probíhá' nebo 'Hotovo'.")

    if not ukol_existuje(id_ukolu, conn):
        raise ValueError("Zadaný úkol neexistuje.")

    kurzor = conn.cursor()
    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (stav[novy_stav], id_ukolu))
    conn.commit()
    kurzor.close()
    print(" Úkol aktualizován.")



def odstranit_ukol(id_ukolu, conn):
    if not ukol_existuje(id_ukolu, conn):
        raise ValueError("Zadaný úkol neexistuje.")

    kurzor = conn.cursor()

    kurzor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    conn.commit()
    kurzor.close()
    print(" Úkol odstraněn.")


def hlavni_menu():

    conn = pripojeni()
    vytvor_tabulku(conn)

    while True:
        print("\n HLAVNÍ MENU")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyber možnost (1-5): ").strip()

    
        if volba == '1':
            nazev = input("Zadej název úkolu: ")
            popis = input("Zadej popis úkolu: ")
            pridat_ukol(nazev, popis, conn)
        elif volba == '2':
            zobrazit_ukoly(conn)
        elif volba == '3':
            id_ukolu = int(input("Zadej ID úkolu: "))
            novy_stav = input("Zadej nový stav (Probíhá / Hotovo): ")
            aktualizovat_ukol(id_ukolu, novy_stav, conn)
        elif volba == '4':
            id_ukolu = int(input("Zadej ID úkolu: "))
            odstranit_ukol(id_ukolu, conn)
        elif volba == '5':
            print("Program končí")
            break
        else:
                print("Neplatná volba, zadejte číslo mezi 1 a 5.")
    conn.close()

if __name__ == "__main__":
    hlavni_menu()