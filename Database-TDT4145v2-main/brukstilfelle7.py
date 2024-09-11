import sqlite3

def brukstilfelle7():
    print("Denne funksjonen sjekker hvilke skuespillere en bestemt skuespiller har spilt med")

    conn = sqlite3.connect("DB2.db")
    cursor = conn.cursor()

    AnsattID = int(input("Skriv inn AnsattID? "))
    print("Du valgte AnsattID: ", AnsattID)

    # Henter skuespillerens navn basert på SkuespillerID
    cursor.execute("SELECT Navn FROM Ansatte WHERE AnsattID = ? AND Stilling = 'Skuespiller'", (AnsattID,))
    resultat = cursor.fetchone()
    if resultat:
        skuespiller_navn = resultat[0]
        print(f"{skuespiller_navn} har spilt med følgende skuespillere i følgende stykker og akter: \n")
    else:
        cursor.execute("SELECT Stilling FROM Ansatte WHERE AnsattID = ?", (AnsattID,))
        stilling = cursor.fetchone()
        if stilling:
            print(f"Skuespiller ikke funnet. Personen har denne stillingen: {stilling[0]}")
        else:
            print("Finnes ikke en ansatt med denne AnsattID-en")
        return
    # Bruker parameterisert spørring for å hente AktNummer og StykkeNavn basert på AnsattID
    cursor.execute("SELECT DISTINCT Aktnummer, StykkeNavn FROM SpillerIAkt WHERE AnsattID = ?", (AnsattID,))
    oppsetninger = cursor.fetchall()
    for Akt, Stykke in oppsetninger:
        # Henter tilleggsinformasjon basert på Akt og Stykke med en JOIN på Ansatte for å få skuespillernes navn, ekskluderer valgt AnsattID
        cursor.execute("""
            SELECT DISTINCT SpillerIAkt.Aktnummer, SpillerIAkt.StykkeNavn, SpillerIAkt.AnsattID, Ansatte.Navn, SpillerIAkt.RolleNavn 
            FROM SpillerIAkt 
            JOIN Ansatte ON SpillerIAkt.AnsattID = Ansatte.AnsattID 
            WHERE SpillerIAkt.AktNummer = ? AND SpillerIAkt.StykkeNavn = ? AND SpillerIAkt.AnsattID != ?""", (Akt, Stykke, AnsattID))
        skuespillere = cursor.fetchall()
        if skuespillere:
            print(f"Akt {Akt}: {Stykke}")
            for _, _, ansatt_id, ansatt_navn, rolle_navn in skuespillere:
                print(f"  Ansatt ID: {ansatt_id}, Navn: {ansatt_navn}, Rolle: {rolle_navn}")
            print()

brukstilfelle7()
