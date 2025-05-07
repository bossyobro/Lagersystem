from db import *


# Just to remind me how to interact with the database

# sql_statement = "INSERT INTO varer (navn, varenummer, pris, antall, kategori) VALUES (%s, %s, %s, %s, %s)"
# vals = ("kamera", 1001, 20, 1, "elektronikk")
# mycursor.execute(sql_statement, vals)

# dbconn.commit()



def print_ui():
    print("Velkommen til Varehåndteringssystemet!")
    print("1. Legg til en ny vare")
    print("2. Vis alle varer")
    print("3. Oppdater en vare")
    print("4. Slett en vare")
    print("5. Avslutt")
    userInput = int(input("Pick from 1-5: "))
    return userInput

userInput = print_ui()


if userInput == 1:
    navn = input("navn: ")
    
    # Check if the item name already exists in the database
    mycursor.execute("SELECT * FROM varer WHERE navn = %s", (navn,))
    existing_item = mycursor.fetchone()
    if existing_item:
        print("En vare med dette navnet eksisterer allerede. Vennligst velg et annet navn.")
        print_ui()
    else:
        pris = input("Pris: ")
        antall = input("Antall: ")
        kategori = input ("A) elektronikk, B) klær, C) kontor [A/B/C]? : ")
        if kategori == "A":
            kategori = "elektronikk"
        elif kategori == "B":
            kategori = "klaer"
        elif kategori == "C":
            kategori = "kontor"
        else:
            print("You didnt pick any of the options! Go back as punishment!")
            print_ui()

    # Varenummer blir basically autogeneret her. Starter på 1000 og incrementer med 1 for alle nye items
    mycursor.execute("SELECT MAX(varenummer) FROM varer")
    result = mycursor.fetchone()
    if result[0] is None:
        varenummer = 1000
    else:
        varenummer = result[0] + 1
    

    
    sql_statement = "INSERT INTO varer (navn, varenummer, pris, antall, kategori) VALUES (%s, %s, %s, %s, %s)"
    vals = (navn, varenummer, pris, antall, kategori)
    mycursor.execute(sql_statement, vals)
    dbconn.commit()

    # En sjekk for om den ble adda i databasen eller ikke.
    mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
    added_item = mycursor.fetchone()
    if added_item:
        print("Varen ble lagt til i databasen:")
        print(added_item)
    else:
        print("Noe gikk galt. Varen ble ikke lagt til.")

elif userInput == 2:
    mycursor.execute("SELECT * FROM varer")
    varer = mycursor.fetchall()
    if varer:
        print("Varer i lageret:")
        print(f"{'Navn':<20}{'Varenummer':<15}{'Pris':<10}{'Antall':<10}{'Kategori':<15}")
        print("-" * 70)
        for vare in varer:
            print(f"{vare[0]:<20}{vare[1]:<15}{vare[2]:<10}{vare[3]:<10}{vare[4]:<15}")
        print_ui()
    else:
        print("Ingen varer funnet i lageret.")
        print_ui()

elif userInput == 5:
    quit()
