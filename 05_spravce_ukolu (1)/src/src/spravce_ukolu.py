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


def pridat_ukol():
    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if not nazev:
            print("Název úkolu nesmí být prázdný.")
            continue
        popis = input("Zadejte popis úkolu: ").strip()
        if not popis:
            print("Popis úkolu nesmí být prázdný.")
            continue


        conn = pripojeni()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ukoly (nazev, popis)
            VALUES (%s, %s)
        """, (nazev, popis))

        conn.commit()
        cursor.close()
        conn.close()
        print("Úkol byl úspěšně přidán.")
        break


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
            print(f"ID: {ukol[0]}, Název: {ukol[1]}")

    
    kurzor.close()
    conn.close()


def aktualizovat_ukol():
    conn = pripojeni()
    kurzor = conn.cursor()

    id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat: "))
    
    kurzor.execute("SELECT id, stav FROM ukoly WHERE id = %s", (id_ukolu,))
    ukol = kurzor.fetchall()

    if not ukol:
        print("Nejsou žádné úkoly k aktualizaci.")
        return
    
    print("\nSeznam úkolů:")
    for ukol in ukol:
        print(f"{ukol[0]}: {ukol[1]} (Stav: {ukol[2]})")

    while True:
        try:
            

            if not any(ukol[0] == id_ukolu for ukol in ukol):
                print("Zadané ID úkolu neexistuje. Zkuste to znovu.")
                continue

            novy_stav = input("Zadejte nový stav (Probíhá / Hotovo): ").capitalize()
            if novy_stav not in ["Probíhá", "Hotovo"]:
                print("Neplatný stav. Zadejte buď 'Probíhá' nebo 'Hotovo'.")
                continue

            kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
            conn.commit()
            print(f"Úkol {id_ukolu} byl úspěšně aktualizován na stav '{novy_stav}'.")
            break

        except ValueError:
            print("Zadejte platné číslo ID.")

    kurzor.close()
    conn.close()


def odstranit_ukol():
    conn = pripojeni()
    kurzor = conn.cursor()

    kurzor.execute("SELECT id, nazev FROM ukoly")
    ukoly = kurzor.fetchall()

    if not ukoly:
        print("Žádné úkoly nejsou k odstranění.")
        kurzor.close()
        conn.close()
        return
    
    print("\n Seznam úkolů:")
    for ukol in ukoly:
        print(f"{ukol[0]}: {ukol[1]}")

    while True:
        zobrazit_ukoly()
        
        cislo_ukolu = input("Zadejte číslo úkolu, který chcete odstranit: ").strip()
        if cislo_ukolu == "":
            print("Číslo úkolu nesmí být prázdné.")
            continue

        if not cislo_ukolu.isdigit():
            print("Zadejte platné číslo.")
            continue

        id_ukolu = int(cislo_ukolu)
        if not any(ukol[0] == id_ukolu for ukol in ukoly):
            print("Zadané ID úkolu neexistuje.")
            continue
        
        potvrzeni_odstraneni = input(f"Opravdu chcete odstranit úkol {id_ukolu}? (a/n): ").lower()

        if potvrzeni_odstraneni == 'a':
            kurzor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            conn.commit()
            print("Úkol byl odstraněn.")
            
        else:
            print("Odstranění zrušeno.")
        break

    kurzor.close()
    conn.close()
    print("Odstranění zrušeno.")



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