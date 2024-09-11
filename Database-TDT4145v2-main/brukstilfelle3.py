import sqlite3
import numpy as np
def brukstilfelle3(antall_billetter = 9):
    con = sqlite3.connect("DB2.db")
    cursor = con.cursor()

    with open("gamle-scene.txt", "r") as f:
        lines = f.readlines()
        ferdig = False

        cursor.execute(f"SELECT OppsetningsID FROM Oppsetning WHERE Dato = '2024-02-03' AND StykkeNavn = 'Størst av alt er kjærligheten'")
        OppsetningsID = cursor.fetchall()
        OppsetningsID = int(OppsetningsID[0][0])
        KundeID = 1
        Type = "Ordinær"

        cursor.execute(f"SELECT Pris FROM Priser WHERE OppsetningsID = '{OppsetningsID}' AND Type = '{Type}'")
        pris_for_en_billett = cursor.fetchall()

        print("Velkommen til billettkjøp!")
        while ferdig == False:
            område = (input("Velg et område blant Galleri, Parkett og Balkong: "))
            print("Du valgte: ",område)

            if område == 'Galleri':
                linje_index = 5 #Det er her Balkong begynner
                rad = int(input("Velg en rad på Galleri (1-3): "))
                print("Du valgte rad: ", rad)

                if rad < 1 or rad > 3:
                    print("Dette er ikke en gyldig rad. Velg på nytt.")
                    pass
                else:
                    ledige_seter = lines[linje_index-rad].count('0') #Teller antall 0-er i strengen. Dette tilsvarer ledige seter
                    if ledige_seter >= antall_billetter:
                        print(f"Denne raden har {ledige_seter} ledige seter så du kan kjøpe {antall_billetter} voksenbilletter.")
                        print(f"Dette er prisen for 9 ordinære billetter: {int(pris_for_en_billett[0][0]) * antall_billetter}kr")

                        #Må velge 9 seter fra raden og legge de inn i databasen. Finner de 9 første ledige setene fra venstre
                        i = 0
                        stolnr = 1
                        while i < 9:
                            if lines[linje_index-rad][stolnr-1] == '0':
                                i += 1
                                cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{rad}', 'Galleri',{OppsetningsID},{KundeID})")
                                cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{rad}', 'Galleri')")
                                con.commit()
                            else:
                                pass
                            stolnr += 1
                        ferdig = True
                        pass
                    else:
                        print(f"Denne raden har {ledige_seter} ledige seter så du må velge en annen rad.")
                        pass
                    
            elif område == "Balkong":
                linje_index = 10 #Det er her Parkett begynner
                rad = int(input("Velg en rad på Balkong (1-4): "))
                print("Du valgte rad: ", rad)

                if rad < 1 or rad > 4:
                    print("Dette er ikke en gyldig rad. Velg på nytt.")
                    pass
                else:

                    ledige_seter = lines[linje_index-rad].count('0')
                    if ledige_seter >= antall_billetter:

                        print(f"Denne raden har {ledige_seter} ledige seter så du kan kjøpe  {antall_billetter} voksenbilletter.")
                        print(f"Dette er prisen for 9 ordinære billetter: {int(pris_for_en_billett[0][0]) *  antall_billetter}kr")
                        i = 0
                        stolnr = 1
                        while i < 9:
                            if lines[linje_index-rad][stolnr-1] == '0':
                                i += 1
                                cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{rad}', 'Balkong',{OppsetningsID},{KundeID})")
                                cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{rad}', 'Balkong')")
                                con.commit()
                            else:
                                pass
                            stolnr += 1
                        ferdig = True
                        pass
                    else:
                        print(f"Denne raden har {ledige_seter} ledige seter så du må velge en annen rad.")
                        pass
                    pass

            elif område == "Parkett":
                    linje_index = 21 #Det er her Parkett slutter
                    rad = int(input("Velg en rad på Parkett (1-10): "))
                    print("Du valgte rad: ", rad)

                    if rad < 1 or rad > 10:
                        print("Dette er ikke en gyldig rad. Velg på nytt.")
                        pass

                    else:
                        ledige_seter = lines[linje_index-rad].count('0')
                        if ledige_seter >= antall_billetter:
                            print(f"Denne raden har {ledige_seter} ledige seter så du kan kjøpe  {antall_billetter} voksenbilletter.")
                            print(f"Dette er prisen for 9 ordinære billetter: {int(pris_for_en_billett[0][0]) *  antall_billetter}kr")
                            i = 0
                            stolnr = 1
                            while i < 9:
                                if lines[linje_index-rad][stolnr-1] == '0':
                                    i += 1
                                    cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{rad}', 'Parkett',{OppsetningsID},{KundeID})")
                                    cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{rad}', 'Parkett')")
                                    con.commit()
                                else:
                                    pass
                                stolnr += 1

                            ferdig = True
                            pass
                        else:
                            print(f"Denne raden har {ledige_seter} ledige seter så du må velge en annen rad.")
                            pass
                        pass
brukstilfelle3()