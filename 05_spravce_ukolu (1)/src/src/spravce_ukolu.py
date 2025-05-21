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


def vytvor_tabulku():
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


def pridat_ukol(nazev, popis):
    if not nazev.strip():
        raise ValueError("Název úkolu nesmí být prázdný.")
    if not popis.strip():
        raise ValueError("Popis úkolu nesmí být prázdný.")
    
    conn = pripojeni()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ukoly (nazev, popis)
        VALUES (%s, %s)
    """, (nazev, popis))
    conn.commit()
    cursor.close()
    conn.close()


def zobrazit_ukoly():
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("SELECT id, nazev FROM ukoly")
    vysledky = kurzor.fetchall()

    kurzor.close()
    conn.close()

    return vysledky


def aktualizovat_ukol(id_ukolu, novy_stav):
    if novy_stav not in ["Probíhá", "Hotovo"]:
        raise ValueError("Neplatný stav. Zadejte 'Probíhá' nebo 'Hotovo'.")

    conn = pripojeni()
    kurzor = conn.cursor()
    kurzor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
    if kurzor.fetchone() is None:
        raise ValueError("Zadaný úkol neexistuje.")

    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
    conn.commit()
    kurzor.close()
    conn.close()



def odstranit_ukol(id_ukolu):
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
    if kurzor.fetchone() is None:
        raise ValueError("Zadaný úkol neexistuje.")

    kurzor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))

    conn.commit()
    kurzor.close()
    conn.close()

def hlavni_menu():
    vytvor_tabulku()
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