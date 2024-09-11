import sqlite3
import numpy as np



#Dette er en funksjon som tar inn en dato fra brukeren og skriver ut forestillingene som er satt opp den dagen og printer alle billettene som er solgt
def brukstilfelle4():
    
    con = sqlite3.connect("DB2.db")
    cursor = con.cursor()

    dato = input("Skriv inn en dato du ønsker å vite hvilke oppsetninger som går på (YYYY-MM-DD): ")
    
    #Alle forestillingene som er satt opp den dagen
    cursor.execute("SELECT * FROM Oppsetning WHERE Dato = ?", (dato,))
    oppsetninger = cursor.fetchall()

    if len(oppsetninger) == 0:
        print("På denne datoen er det ingen oppsetninger.")

    for oppsetning in oppsetninger:
        print(f'På {dato} går {oppsetning[-1]} klokken {oppsetning[2]}')

        #Alle billettene som er solgt til hver forestilling
        cursor.execute("SELECT * FROM Billett where OppsetningsID = ?", (oppsetning[0],))
        billetter = cursor.fetchall()
        print(f"Til denne oppsetning ble det solgt {len(billetter)} biletter.")
        
brukstilfelle4()
