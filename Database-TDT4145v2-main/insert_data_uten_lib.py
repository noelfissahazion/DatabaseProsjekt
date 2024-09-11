import numpy as np
import sqlite3

con = sqlite3.connect("DB2.db")
cursor = con.cursor()

def tom_database():
    #Henter ut alle tabellene og itererer gjennom og tømmer de
    cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DELETE FROM {table[0]}")
    con.commit()

#Denne funksjonen innsetter manuelt de enkleste tingene i databasen, slik som saler og stykker.
def insert_diverse():
    cursor.execute("INSERT INTO Sal (Navn) VALUES ('Hovedscene')")
    cursor.execute("INSERT INTO Sal (Navn) VALUES ('Gamle scene')")
    
    cursor.execute("INSERT INTO Stykke (StykkeNavn, Forfatter) VALUES ('Kongsemnene', 'Henrik Ibsen')")
    cursor.execute("INSERT INTO Stykke (StykkeNavn, Forfatter) VALUES ('Størst av alt er kjærligheten', 'Jonas Corell Petersen')")

    oppsetninger = [
        (1,'2024-02-01','19:00','Hovedscene','Kongsemnene'),
        (2,'2024-02-02','19:00','Hovedscene','Kongsemnene'),
        (3,'2024-02-03','19:00','Hovedscene','Kongsemnene'),
        (4,'2024-02-05','19:00','Hovedscene','Kongsemnene'),
        (5,'2024-02-06','19:00','Hovedscene','Kongsemnene'),
        (6,'2024-02-03','18:30','Gamle scene','Størst av alt er kjærligheten'),
        (7,'2024-02-06','18:30','Gamle scene','Størst av alt er kjærligheten'),
        (8,'2024-02-07','18:30','Gamle scene','Størst av alt er kjærligheten'),
        (9,'2024-02-12','18:30','Gamle scene','Størst av alt er kjærligheten'),
        (10,'2024-02-13','18:30','Gamle scene','Størst av alt er kjærligheten'),
        (11,'2024-02-14','18:30','Gamle scene','Størst av alt er kjærligheten')
    ]

    for oppsetning in oppsetninger:
        cursor.execute(f"INSERT INTO Oppsetning (OppsetningsID, Dato, Klokkeslett,SalNavn,StykkeNavn) VALUES ({oppsetning[0]}, '{oppsetning[1]}', '{oppsetning[2]}', '{oppsetning[3]}', '{oppsetning[4]}')")


    cursor.execute("INSERT INTO Akt (AktNummer, StykkeNavn, AktNavn) VALUES (1,'Kongsemnene', 'Første')")
    cursor.execute("INSERT INTO Akt (AktNummer, StykkeNavn, AktNavn) VALUES (2,'Kongsemnene', 'Andre')")
    cursor.execute("INSERT INTO Akt (AktNummer, StykkeNavn, AktNavn) VALUES (3,'Kongsemnene', 'Tredje')")
    cursor.execute("INSERT INTO Akt (AktNummer, StykkeNavn, AktNavn) VALUES (4,'Kongsemnene', 'Fjerde')")
    cursor.execute("INSERT INTO Akt (AktNummer, StykkeNavn, AktNavn) VALUES (5,'Kongsemnene', 'Femte')")
    cursor.execute("INSERT INTO Akt (AktNummer, StykkeNavn, AktNavn) VALUES (1,'Størst av alt er kjærligheten', 'Første')")

    priser_kongsemnene = [
        ('Ordinær',450),
        ('Honnør',380),
        ('Student',280),
        ('Gruppe 10',420),
        ('Gruppe honnør 10',360)]
    priser_storst = [
        ('Ordinær',350),
        ('Honnør',300),
        ('Student',220),
        ('Barn',220),
        ('Gruppe 10',320),
        ('Gruppe 10 honnør',270),
    ]

    for oppsetning in oppsetninger:

        #Sjekker hvilket stykke det er
        if oppsetning[-1] == "Kongsemnene":
            for pris in priser_kongsemnene:
                cursor.execute(f"INSERT INTO Priser (OppsetningsID, Type, Pris) VALUES ({oppsetning[0]}, '{pris[0]}', {pris[1]})")
        else:
            for pris in priser_storst:
                cursor.execute(f"INSERT INTO Priser (OppsetningsID, Type, Pris) VALUES ({oppsetning[0]}, '{pris[0]}', {pris[1]})")



    #Sette inn seter:
    with open("hovedscenen.txt", "r") as f:
        lines = f.readlines()
        for linjenummer, line in enumerate(lines):
            line = line.strip()
            if line == "Galleri":
                #Starte en egen iterasjon kun gjennom Galleri, og så utføre operasjoner her
                stolnr = 505
                #Lage en variabel som begynner å telle fra starten av Galleri. Slik vet vi hvor vi er inni Galleri.
                iterasjoner_inni_galleri = 0
                for rad in lines[1+linjenummer:]:
                    #Stopper hvis vi kommer til parkett
                    if lines[1+linjenummer+iterasjoner_inni_galleri].strip() == "Parkett":
                        break
                    if (1+linjenummer+iterasjoner_inni_galleri) < 4:
                        radnr = 'Nedre'
                    else:
                        radnr = 'Øvre'
                    for i in range(len(rad)-1):
                        if rad[i] == "x":
                            stolnr += 1
                            pass
                        cursor.execute(f"INSERT INTO Sete (StolNr, RadNr, Område,SalNavn) VALUES ('{stolnr}', '{radnr}', 'Galleri','Hovedscenen')")
                        con.commit()
                        stolnr += 1
                        
                    iterasjoner_inni_galleri += 1
            if line == "Parkett":
                stolnr = 477
                radnr = 18
                for rad in lines[1+linjenummer:]:
                    for i in range(len(rad)-1):
                        if rad[i] != "x": 
                            cursor.execute(f"INSERT INTO Sete (StolNr, RadNr, Område,SalNavn) VALUES ('{stolnr}', '{radnr}', 'Parkett','Hovedscenen')")
                            con.commit()
                        stolnr += 1
                    stolnr -= 56
                    radnr -= 1
    

    with open("gamle-scene.txt", "r") as f:
            lines = f.readlines()
        
            for linjenummer, line in enumerate(lines):
                line = line.strip()

                if line == "Galleri":

                    #Starte en egen iterasjon kun gjennom Galleri, og så utføre operasjoner her
                    radnr = 3
                    iterasjoner_inni_galleri = 0
                    for rad in lines[1+linjenummer:]:
                        stolnr = 1
                        #Stopper hvis vi kommer til Balkong
                        if lines[1+linjenummer+iterasjoner_inni_galleri].strip() == "Balkong":
                            break
                        for i in range(len(rad)-1):
                            cursor.execute(f"INSERT INTO Sete (StolNr, RadNr, Område,SalNavn) VALUES ('{stolnr}', '{radnr}', 'Galleri','Gamle scene')")
                            con.commit()
                            stolnr += 1
                        radnr -= 1
                        iterasjoner_inni_galleri += 1
                if line == "Balkong":

                    radnr = 4
                    iterasjoner_inni_galleri = 0
                    for rad in lines[1+linjenummer:]:
                        stolnr = 1
                        #Stopper hvis vi kommer til parkett
                        if lines[1+linjenummer+iterasjoner_inni_galleri].strip() == "Parkett":
                            break
                        for i in range(len(rad)-1):
                            cursor.execute(f"INSERT INTO Sete (StolNr, RadNr, Område,SalNavn) VALUES ('{stolnr}', '{radnr}', 'Balkong','Gamle scene')")
                            con.commit()
                            stolnr += 1
                        radnr -= 1
                        iterasjoner_inni_galleri += 1


                if line == "Parkett":
                    radnr = 10
                    iterasjoner_inni_galleri = 0                    
                    for rad in lines[1+linjenummer:]:
                        stolnr = 1
                        #Stopper hvis vi kommer til parkett
                        for i in range(len(rad)-1):                           
                            cursor.execute(f"INSERT INTO Sete (StolNr, RadNr, Område,SalNavn) VALUES ('{stolnr}', '{radnr}', 'Parkett','Gamle scene')")
                            con.commit()
                            stolnr += 1
                        radnr -= 1
                        iterasjoner_inni_galleri += 1

    
    #For å legge inn solgte stoler og gjøre kjøp må vi legge inn en standardbruker i databasen
    cursor.execute(f"INSERT INTO Kundeprofil (KundeID, TlfNr, Navn, Adresse, Epost) VALUES ({1}, '12345678','Navn Navnesen','Storgata 1','test@gmail.com')")
    con.commit()   
    

def storst_av_alt():


    kunstnerisk_dict = [{'Name': 'Jonas Corell Petersen', 'Role': 'Regi'}, {'Name': 'David Gehrt', 'Role': 'Scenografi og kostymer'}, {'Name': 'Gaute Tønder', 'Role': 'Musikalsk ansvarlig'}, {'Name': 'Magnus Mikaelsen', 'Role': 'Lysdesign'}, {'Name': 'Kristoffer Spender', 'Role': 'Dramaturg'}]
    medvirkende_dict = [{'Name': 'Sunniva Du Mond Nordal', 'Role': 'Sunniva Du Mond Nordal'}, {'Name': 'Jo Saberniak', 'Role': 'Jo Saberniak'}, {'Name': 'Marte M. Steinholt', 'Role': 'Marte M. Steinholt'}, {'Name': 'Tor Ivar Hagen', 'Role': 'Tor Ivar Hagen'}, {'Name': 'Trond-Ove Skrødal', 'Role': 'Trond-Ove Skrødal'}, {'Name': 'Natalie Grøndahl Tangen', 'Role': 'Natalie Grøndahl Tangen'}, {'Name': 'Åsmund Flaten', 'Role': 'Åsmund Flaten'}]

    #Setter inn skuespillerne fra medvirkende-seksjonen
    for i in range(len(medvirkende_dict)):
        AnsattID = i+1
        Navn = medvirkende_dict[i]["Name"]
        Epost = 'fornavn@etternavn.no'
        Ansattstatus = 'heltid'
        Stilling = 'Skuespiller'
        #Skrur av fremmednøkkelrestriksjoner for å sette inn i Ansatte- og Stillinger-tabellen.
        cursor.execute(f"PRAGMA foreign_keys = OFF;")
        cursor.execute(f"INSERT INTO Ansatte (AnsattID, Navn, Epost,Ansattstatus ,Stilling) VALUES ({AnsattID},'{Navn}','{Epost}','{Ansattstatus}','{Stilling}')")
        cursor.execute(f"INSERT INTO Stillinger (Stilling, AnsattID) VALUES ('{Stilling}',{AnsattID})")
        cursor.execute(f"PRAGMA foreign_keys = ON;")
        cursor.execute(f"INSERT INTO Rolle (RolleNavn, AnsattID) VALUES ('{Navn}',{AnsattID})")
        cursor.execute(f"INSERT INTO SpillerRolle (AnsattID,RolleNavn) VALUES ({AnsattID},'{Navn}')")
        con.commit()
        
    cursor.execute("SELECT AnsattID FROM Ansatte")
    rows = cursor.fetchall()
    #Finne ut hvilken AnsattID man skal begynne på
    forrige_ansattid = rows[-1][0]
    for i in range(len(kunstnerisk_dict)):
    
        AnsattID = forrige_ansattid + i + 1
        Navn = kunstnerisk_dict[i]["Name"]
        Epost = 'fornavn@etternavn.no'
        Ansattstatus = 'heltid'
        Stilling = kunstnerisk_dict[i]["Role"]
        cursor.execute(f"PRAGMA foreign_keys = OFF;")
        cursor.execute(f"INSERT INTO Ansatte (AnsattID, Navn, Epost,Ansattstatus ,Stilling) VALUES ({AnsattID},'{Navn}','{Epost}','{Ansattstatus}','{Stilling}')")
        cursor.execute(f"INSERT INTO Stillinger (Stilling, AnsattID) VALUES ('{Stilling}',{AnsattID})")
        cursor.execute(f"PRAGMA foreign_keys = ON;")
        cursor.execute(f"INSERT INTO JobberPå (AnsattID, StykkeNavn) VALUES ('{AnsattID}', 'Størst av alt er kjærligheten')")

        con.commit()

    
    cursor.execute("SELECT OppsetningsID FROM Oppsetning WHERE StykkeNavn = 'Størst av alt er kjærligheten' ")
    oppsetninger = cursor.fetchall()
    #Går gjennom alle oppsetninger
    for i in range(len(oppsetninger)):
        StykkeNavn = 'Størst av alt er kjærligheten'
        OppsetningsID = i+1
        #Siden skuespillerne i Størst av alt er kjærligheten spiller seg selv, kan vi hente ut alle rollene der Rollenavn er lik Navn.
        cursor.execute("SELECT AnsattID, RolleNavn FROM SpillerRolle NATURAL JOIN Ansatte WHERE (Navn == RolleNavn)")
        roller = cursor.fetchall()

        #Går så gjennom ID-en og rollenavnet til alle av disse rollene
        for id, rollenavn in roller:
            #Må nå sette inn Rollenavn og AnsattID til denne rollen
            cursor.execute(f"INSERT INTO SpillerIAkt (AktNummer, StykkeNavn,OppsetningsID,AnsattID,RolleNavn) Values (1,'Størst av alt er kjærligheten',{OppsetningsID},{id},'{rollenavn}')")
        con.commit()



def kongsemnene():
   
    dict_medvirkende = [{'Name': 'Arturo Scotti', 'Role': 'Haakon Haakonssønn'}, {'Name': 'Ingunn Beate Strige Øyen', 'Role': 'Inga fra Vartejg (Haakons mor)'}, {'Name': 'Hans Petter Nilsen', 'Role': 'Skule jarl'}, {'Name': 'Madeleine Brandtzæg Nilsen', 'Role': 'Fru Ragnhild (Skules hustru)'}, {'Name': 'Synnøve Fossum Eriksen', 'Role': 'Margrete (Skules datter)'}, {'Name': 'Emma Caroline Deichmann', 'Role': 'Sigrid (Skules søster)'}, {'Name': 'Emma Caroline Deichmann', 'Role': 'Ingebjørg'}, {'Name': 'Thomas Jensen Takyi', 'Role': 'Biskop Nikolas'}, {'Name': 'Per Bogstad Gulliksen', 'Role': 'Gregorius Jonssønn'}, {'Name': 'Isak Holmen Sørensen', 'Role': 'Paal Flida'}, {'Name': 'Isak Holmen Sørensen', 'Role': 'Trønder'}, {'Name': 'Fabian Heidelberg Lunde', 'Role': 'Baard Bratte'}, {'Name': 'Fabian Heidelberg Lunde', 'Role': 'Trønder'}, {'Name': 'Emil Olafsson', 'Role': 'Jatgeir Skald'}, {'Name': 'Emil Olafsson', 'Role': 'Dagfinn Bonde'}, {'Name': 'Snorre Ryen Tøndel', 'Role': 'Peter (prest og Ingebjørgs sønn)'}]
    dict_kunstnerisk = [{'Name': 'Yury Butusov', 'Role': 'Regi og musikkutvelgelse'}, {'Name': 'Aleksandr Shishkin-Hokusai', 'Role': 'Scenografi og kostymer'}, {'Name': 'Eivind Myren', 'Role': 'Lysdesign'}, {'Name': 'Mina Rype Stokke', 'Role': 'Dramaturg'}]

    cursor.execute("SELECT AnsattID FROM Ansatte")
    rows = cursor.fetchall()
    forrige_ansattid = rows[-1][0]
    
    #Tar de unike navnene og bevarer rekkefølgen
    unike_navn = []
    for i in range(len(dict_medvirkende)):
        if not dict_medvirkende[i]['Name'] in unike_navn:
            unike_navn.append(dict_medvirkende[i]['Name'])
    #Setter inn skuespillere
    for i in range(len(unike_navn)):
        AnsattID = forrige_ansattid + i + 1
        Navn = unike_navn[i]
        Epost = 'fornavn@etternavn.no'
        Ansattstatus = 'heltid'
        Stilling = "Skuespiller"
        cursor.execute(f"PRAGMA foreign_keys = OFF;")
        cursor.execute(f"INSERT INTO Ansatte (AnsattID, Navn, Epost,Ansattstatus ,Stilling) VALUES ({AnsattID},'{Navn}','{Epost}','{Ansattstatus}','{Stilling}')")
        cursor.execute(f"INSERT INTO Stillinger (Stilling, AnsattID) VALUES ('{Stilling}',{AnsattID})")
        cursor.execute(f"PRAGMA foreign_keys = ON;")
        con.commit()

    #Setter inn andre ansatte    
    cursor.execute("SELECT AnsattID FROM Ansatte")
    rows = cursor.fetchall()
    forrige_ansattid = rows[-1][0]
    for i in range(len(dict_kunstnerisk)):
        AnsattID = forrige_ansattid + i + 1
        Navn = dict_kunstnerisk[i]["Name"]
        Epost = 'fornavn@etternavn.no'
        Ansattstatus = 'heltid'
        Stilling = dict_kunstnerisk[i]["Role"]

        cursor.execute(f"PRAGMA foreign_keys = OFF;")
        cursor.execute(f"INSERT INTO Ansatte (AnsattID, Navn, Epost,Ansattstatus ,Stilling) VALUES ({AnsattID},'{Navn}','{Epost}','{Ansattstatus}','{Stilling}')")
        cursor.execute(f"INSERT INTO Stillinger (Stilling, AnsattID) VALUES ('{Stilling}',{AnsattID})")
        cursor.execute(f"PRAGMA foreign_keys = ON;")
        cursor.execute(f"INSERT INTO JobberPå (AnsattID, StykkeNavn) VALUES ('{AnsattID}', 'Kongsemnene')")
        
        con.commit()
    

    for i in range(len(dict_medvirkende)):
        Rolle = dict_medvirkende[i]['Role']
        Navn =  dict_medvirkende[i]['Name']
        cursor.execute(f"SELECT AnsattID From Ansatte WHERE Navn = '{Navn}'")
        AnsattID = cursor.fetchall()[0][0]
        cursor.execute(f"INSERT INTO Rolle (RolleNavn, AnsattID) VALUES ('{Rolle}',{AnsattID})")
        cursor.execute(f"INSERT INTO SpillerRolle (AnsattID,RolleNavn) VALUES ({AnsattID},'{Rolle}')")
        con.commit()
        
    
    #Setter så inn ansatte i enten medvirkende eller skuespillere. Itererer gjennom liste.
    cursor.execute("SELECT AnsattID, Stilling FROM Ansatte")
    alle_ansatte = cursor.fetchall() 
    for id, stilling in alle_ansatte:
        if stilling == 'Skuespiller':
            cursor.execute(f"INSERT INTO Skuespiller (AnsattID) Values ({id})")
        else:
            cursor.execute(f"INSERT INTO Medvirkende (AnsattID, Oppgave) Values ({id}, '{stilling}')")
    con.commit()

    
    #For å legge inn data i 4-veis relasjonen vår er vi nødt til å vite om hvilke roller som spiller i hvilke akter. 
    #Derfor lager vi et dictionary som inneholder alle akter, og hvilke roller som spiller i den gitte akten

    rolle_i_akt = {
        1: ['Haakon Haakonssønn','Dagfinn Bonde','Skule jarl','Paal Flida','Gregorius Jonssønn','Margrete (Skules datter)', 'Inga fra Vartejg (Haakons mor)','Fru Ragnhild (Skules hustru)','Biskop Nikolas','Sigrid (Skules søster)','Baard Bratte','Trønder'],
        2: ['Haakon Haakonssønn','Dagfinn Bonde','Skule jarl','Paal Flida','Gregorius Jonssønn','Margrete (Skules datter)','Sigrid (Skules søster)','Biskop Nikolas','Baard Bratte','Trønder'],
        3: ['Haakon Haakonssønn','Dagfinn Bonde','Skule jarl','Paal Flida','Gregorius Jonssønn','Margrete (Skules datter)','Inga fra Vartejg (Haakons mor)','Biskop Nikolas','Peter (prest og Ingebjørgs sønn)','Baard Bratte','Trønder'],
        4: ['Haakon Haakonssønn','Dagfinn Bonde','Skule jarl','Paal Flida','Gregorius Jonssønn','Margrete (Skules datter)','Jatgeir Skald','Ingebjørg','Peter (prest og Ingebjørgs sønn)','Baard Bratte','Trønder'],
        5: ['Haakon Haakonssønn','Dagfinn Bonde','Skule jarl','Paal Flida','Gregorius Jonssønn','Margrete (Skules datter)','Sigrid (Skules søster)','Fru Ragnhild (Skules hustru)','Peter (prest og Ingebjørgs sønn)','Baard Bratte','Trønder']
    }
    
    cursor.execute("SELECT AktNummer FROM Akt WHERE StykkeNavn = 'Kongsemnene' ")
    aktnummer = cursor.fetchall()
    cursor.execute("SELECT OppsetningsID FROM Oppsetning WHERE StykkeNavn = 'Kongsemnene' ")
    oppsetninger = cursor.fetchall()
    #Går gjennom alle oppsetninger
    for i in range(len(oppsetninger)):
        #For hver oppsetning, går vi igjennom alle aktene
        for j in range(len(aktnummer)):
    
            Aktnummer = j+1
            OppsetningsID = i+1

            #Siden skuespillerne i Kongsemnene ikke spiller seg selv. Kan vi hente ut alle rollene der Rollenavn ikke er lik Navn.
            cursor.execute("SELECT AnsattID, RolleNavn FROM SpillerRolle NATURAL JOIN Ansatte WHERE NOT (Navn == RolleNavn)")
            roller = cursor.fetchall()

            #Går så gjennom ID-en og rollenavnet til alle av disse rollene
            for id, rollenavn in roller:
                #Må sjekke om en gitt rolle er med i akten vi går gjennom
                if rollenavn in rolle_i_akt[j+1]:
                    #Må nå sette inn Rollenavn og AnsattID til denne rollen
                    cursor.execute(f"INSERT INTO SpillerIAkt (AktNummer, StykkeNavn,OppsetningsID,AnsattID,RolleNavn) Values ({Aktnummer},'Kongsemnene',{OppsetningsID},{id},'{rollenavn}')")
            con.commit()



def solgte_billetter_hovedscenen():
    with open("hovedscenen.txt", "r") as f:
        lines = f.readlines()
    
        for linjenummer, line in enumerate(lines):
            line = line.strip()
            if line == "Galleri":
                #Starte en egen iterasjon kun gjennom Galleri, og så utføre operasjoner her
                stolnr = 505
                radnr = 6
                iterasjoner_inni_galleri = 0
                for rad in lines[1+linjenummer:]:
                    #Stopper hvis vi kommer til parkett
                    if lines[1+linjenummer+iterasjoner_inni_galleri].strip() == "Parkett":
                        break
                    if (1+linjenummer+iterasjoner_inni_galleri) < 4:
                        radnr = 'Nedre'
                    else:
                        radnr = 'Øvre'
    
                    for i in range(len(rad)-1):
                        if rad[i] == '1':
                            #Da er denne stolen kjøpt
                            OppsetningsID = 3
                            KundeID = 1
                            cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{radnr}', 'Galleri',{OppsetningsID},{KundeID})")
                            cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{radnr}', 'Galleri')")
                        
                        stolnr += 1
                    iterasjoner_inni_galleri += 1
            
            if line == "Parkett":
                stolnr = 477
                radnr = 18
                for rad in lines[1+linjenummer:]:
                    for i in range(len(rad)-1):
                        if rad[i] == '1':
                            #Da er denne stolen kjøpt
                          
                            OppsetningsID = 3
                            KundeID = 1
                            cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{radnr}', 'Parkett',{OppsetningsID},{KundeID})")
                            cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{radnr}', 'Parkett')")
                        stolnr += 1 
                    stolnr -= 56
                    radnr -= 1            
    con.commit()

def solgte_billetter_gamle_scene():

    with open("gamle-scene.txt", "r") as f:
            lines = f.readlines()
        
            for linjenummer, line in enumerate(lines):
                line = line.strip()
    
                if line == "Galleri":
                    #Starte en egen iterasjon kun gjennom Galleri, og så utføre operasjoner her
                    radnr = 3
                    iterasjoner_inni_galleri = 0
                    for rad in lines[1+linjenummer:]:
                        stolnr = 1
                        #Stopper hvis vi kommer til Balkong
                        if lines[1+linjenummer+iterasjoner_inni_galleri].strip() == "Balkong":
                            break
    
                        for i in range(len(rad)-1):
                            if rad[i] == '1':
                                OppsetningsID = 6
                                KundeID = 1
                                cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{radnr}', 'Galleri',{OppsetningsID},{KundeID})")
                                cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{radnr}', 'Galleri')")
                            stolnr += 1
                        radnr -= 1
                        iterasjoner_inni_galleri += 1
    
                if line == "Balkong":
                    radnr = 4
                    iterasjoner_inni_galleri = 0
    
                    for rad in lines[1+linjenummer:]:
                        stolnr = 1
                        #Stopper hvis vi kommer til parkett
                        if lines[1+linjenummer+iterasjoner_inni_galleri].strip() == "Parkett":
                            break
                        for i in range(len(rad)-1):
                            if rad[i] == '1':
                                OppsetningsID = 6
                                KundeID = 1
                                cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{radnr}', 'Balkong',{OppsetningsID},{KundeID})")
                                cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{radnr}', 'Balkong')")
                            stolnr += 1
                        radnr -= 1
                        iterasjoner_inni_galleri += 1
    
    
                if line == "Parkett":
                    radnr = 10
                    iterasjoner_inni_galleri = 0
                    for rad in lines[1+linjenummer:]:
                        stolnr = 1
                        for i in range(len(rad)-1):
                            if rad[i] == '1':
                                OppsetningsID = 6
                                KundeID = 1
                                cursor.execute(f"INSERT INTO Billett (StolNr, RadNr, Område,OppsetningsID,KundeID) VALUES ('{stolnr}', '{radnr}', 'Parkett',{OppsetningsID},{KundeID})")
                                cursor.execute(f"INSERT INTO BillettTil (OppsetningsID,Type,StolNr, RadNr, Område) VALUES ({OppsetningsID},'Ordinær','{stolnr}', '{radnr}', 'Parkett')")
                            stolnr += 1
                        radnr -= 1
                        iterasjoner_inni_galleri += 1
    con.commit()
    

def insert_full_database():
    tom_database()
    insert_diverse()
    storst_av_alt()
    kongsemnene()
    solgte_billetter_hovedscenen()
    solgte_billetter_gamle_scene()


insert_full_database()