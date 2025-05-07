from db import *
from os import system

def print_ui():
    while True:
        system("cls")
        print("Velkommen til Varehåndteringssystemet!")
        print("1. Legg til en ny vare")
        print("2. Vis alle varer")
        print("3. Søk")
        print("4. Oppdatere en vare")
        print("5. Slett en vare")
        print("6. Avslutt")
        userInput = int(input("Pick from 1-5: "))

        if userInput == 1:
            add_item()
        elif userInput == 2:
            view_items()
        elif userInput == 3:
            search_items()
        elif userInput == 4:
            update_storage()
        elif userInput == 5:
            delete_items()
        elif userInput == 6:
            quit_program()
        else:
            print("Ugyldig valg, prøv igjen.")

def delete_items():
    print("Hvilken vare har du lyst til å slette?")
    varenummer = input("Varenummer: ")

    mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
    item = mycursor.fetchone()

    if item:
        print(f"Vare funnet: Navn: {item[0]}, Pris: {item[2]}, Antall: {item[3]}, Kategori: {item[4]}")
        mycursor.execute("DELETE FROM varer WHERE varenummer = %s", (varenummer,))
        dbconn.commit()

        mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
        deleted_item = mycursor.fetchone()
        if not deleted_item:
            print("Varen ble slettet fra databasen.")
        else:
            print("Noe gikk galt. Varen ble ikke slettet.")
        
    else:
        print("Ingen vare funnet med det oppgitte varenummeret.")
    return_to_menu()

def update_storage():
    print("Hvilken vare har du lyst til å oppdatere?")
    varenummer = input("Varenummer: ")

    mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
    item = mycursor.fetchone()

    if item:
        print(f"Vare funnet: Navn: {item[0]}, Pris: {item[2]}, Antall: {item[3]}, Kategori: {item[4]}")
        ny_pris = input("Ny pris (trykk enter for å beholde nåværende): ")
        ny_antall = input("Nytt antall (trykk enter for å beholde nåværende): ")

        if ny_pris:
            mycursor.execute("UPDATE varer SET pris = %s WHERE varenummer = %s", (ny_pris, varenummer))

        if ny_antall:
            mycursor.execute("UPDATE varer SET antall = %s WHERE varenummer = %s", (ny_antall, varenummer))

        dbconn.commit()
        print("Varen ble oppdatert.")
    else:
        print("Ingen vare funnet med det oppgitte varenummeret.")

    return_to_menu()

def add_item():
    navn = input("navn: ")

    # Check if the item name already exists in the database
    mycursor.execute("SELECT * FROM varer WHERE navn = %s", (navn,))
    existing_item = mycursor.fetchone()

    if existing_item:
        print("En vare med dette navnet eksisterer allerede. Vennligst velg et annet navn.")
        return print_ui()
    else:
        pris = input("Pris: ")
        antall = input("Antall: ")
        kategori = input("A) elektronikk, B) klær, C) kontor [A/B/C]? : ")
        if kategori == "A":
            kategori = "elektronikk"
        elif kategori == "B":
            kategori = "klaer"
        elif kategori == "C":
            kategori = "kontor"
        else:
            print("You didn't pick any of the options! Go back as punishment!")
            return print_ui()

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
    
    return_to_menu()

def view_items():
    mycursor.execute("SELECT * FROM varer")
    varer = mycursor.fetchall()
    if varer:
        print("Varer i lageret:")
        print(f"{'Navn':<20}{'Varenummer':<15}{'Pris':<10}{'Antall':<10}{'Kategori':<15}")
        print("-" * 70)
        for vare in varer:
            print(f"{vare[0]:<20}{vare[1]:<15}{vare[2]:<10}{vare[3]:<10}{vare[4]:<15}")
    else:
        print("Ingen varer funnet i lageret.")

    return_to_menu()

def search_items():
    varenummer = input("Skriv inn varenummer for å søke: ")
    mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
    result = mycursor.fetchone()
    if result:
        print("Vare funnet:")
        print(f"Navn: {result[0]}, Varenummer: {result[1]}, Pris: {result[2]}, Antall: {result[3]}, Kategori: {result[4]}")
    else:
        print("Ingen vare funnet med det oppgitte varenummeret.")
    return_to_menu()

def quit_program():
    print("Avslutter programmet.")
    quit()

def return_to_menu():
    enter = input("Press enter to continue... ")

    if enter == "":
        return print_ui()
    else:
        print("Sorry, it seems something went wrong")
        quit()



print_ui()
