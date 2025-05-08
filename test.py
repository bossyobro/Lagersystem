from db import *
from os import system


class InventoryApp:
    def __init__(self):
        self.user = None
        self.logged_in = False

    def run(self):
        self.user_auth()

    def user_auth(self):
        print("Velkommen til Varehåndteringssystemet!")
        print("Vennligst logg inn for å fortsette.")
        username = input("Brukernavn: ")
        password = input("Passord: ")

        mycursor.execute("SELECT * FROM brukere WHERE username = %s AND password = %s", (username, password))
        user = mycursor.fetchone()

        if user:
            self.user = user
            self.logged_in = True
            print("Login Sucessfull!")
            self.print_ui()
        else:
            print("Login Unsucessfull, try again!")
            input("Press enter to continue... ")
            self.user_auth()

    def print_ui(self):
        mycursor.execute("SELECT user_type FROM brukere WHERE username = %s", (self.user[1],))
        user_type = mycursor.fetchone()

        if user_type[0] == "Admin":
            self.admin_ui()
        else:
            self.worker_ui()

    def worker_ui(self):
        while True:
            print("Velkommen til Varehåndteringssystemet!")
            print("1. Vis alle varer")
            print("2. Søk")
            print("3. Oppdatere en vare")
            print("4. Avslutt")
            userInput = int(input("Pick from 1-4: "))

            if userInput == 1:
                self.view_items()
            elif userInput == 2:
                self.search_items()
            elif userInput == 3:
                self.update_storage()
            elif userInput == 4:
                self.quit_program()
            else:
                print("Ugyldig valg, prøv igjen.")

    def admin_ui(self):
        while True:
            print("Velkommen til Varehåndteringssystemet!")
            print("1. Legg til en ny vare")
            print("2. Vis alle varer")
            print("3. Søk")
            print("4. Oppdatere en vare")
            print("5. Slett en vare")
            print("6. Avslutt")
            userInput = int(input("Pick from 1-6: "))

            if userInput == 1:
                self.add_item()
            elif userInput == 2:
                self.view_items()
            elif userInput == 3:
                self.search_items()
            elif userInput == 4:
                self.update_storage()
            elif userInput == 5:
                self.delete_items()
            elif userInput == 6:
                self.quit_program()
            else:
                print("Ugyldig valg, prøv igjen.")

    def view_items(self):
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
        self.return_to_menu()

    def search_items(self):
        varenummer = input("Skriv inn varenummer for å søke: ")
        mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
        result = mycursor.fetchone()
        if result:
            print("Vare funnet:")
            print(f"Navn: {result[0]}, Varenummer: {result[1]}, Pris: {result[2]}, Antall: {result[3]}, Kategori: {result[4]}")
        else:
            print("Ingen vare funnet med det oppgitte varenummeret.")
        self.return_to_menu()

    def update_storage(self):
        varenummer = input("Hvilken vare har du lyst til å oppdatere?\nVarenummer: ")

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
        self.return_to_menu()

    def delete_items(self):
        varenummer = input("Hvilken vare har du lyst til å slette?\nVarenummer: ")

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
        self.return_to_menu()

    def add_item(self):
        navn = input("Navn: ")

        mycursor.execute("SELECT * FROM varer WHERE navn = %s", (navn,))
        existing_item = mycursor.fetchone()

        if existing_item:
            print("En vare med dette navnet eksisterer allerede. Vennligst velg et annet navn.")
            return self.print_ui()

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
            print("Du valgte ikke et gyldig alternativ!")
            return self.print_ui()

        mycursor.execute("SELECT MAX(varenummer) FROM varer")
        result = mycursor.fetchone()
        varenummer = 1000 if result[0] is None else result[0] + 1

        sql = "INSERT INTO varer (navn, varenummer, pris, antall, kategori) VALUES (%s, %s, %s, %s, %s)"
        vals = (navn, varenummer, pris, antall, kategori)
        mycursor.execute(sql, vals)
        dbconn.commit()

        mycursor.execute("SELECT * FROM varer WHERE varenummer = %s", (varenummer,))
        added_item = mycursor.fetchone()

        if added_item:
            print("Varen ble lagt til i databasen:")
            print(added_item)
        else:
            print("Noe gikk galt. Varen ble ikke lagt til.")
        self.return_to_menu()

    def quit_program(self):
        print("Avslutter programmet.")
        quit()

    def return_to_menu(self):
        enter = input("Trykk enter for å fortsette... ")
        if enter == "":
            self.print_ui()
        else:
            print("Ugyldig inndata. Avslutter.")
            quit()



if __name__ == "__main__":
    app = InventoryApp()
    app.run()
