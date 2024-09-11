BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Ansatte" (
	"AnsattID"	INTEGER,
	"Navn"	TEXT,
	"Epost"	TEXT,
	"Ansattstatus"	TEXT,
	"Stilling"	TEXT NOT NULL,
	PRIMARY KEY("AnsattID"),
	FOREIGN KEY("Stilling") REFERENCES "Stilling"("Stilling") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Stillinger" (
	"Stilling"	TEXT,
	"AnsattID"	INTEGER NOT NULL,
	--PRIMARY KEY("Stilling"),
	PRIMARY KEY("Stilling","AnsattID"),
	FOREIGN KEY("AnsattID") REFERENCES "Ansatte"("AnsattID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Medvirkende" (
	"AnsattID"	INTEGER,
	"Oppgave"	TEXT,
	PRIMARY KEY("AnsattID"),
	FOREIGN KEY("AnsattID") REFERENCES "Ansatte"("AnsattID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Stykke" (
	"StykkeNavn"	TEXT,
	"Forfatter"	TEXT,
	PRIMARY KEY("StykkeNavn")
);
CREATE TABLE IF NOT EXISTS "JobberPå" (
	"AnsattID"	INTEGER,
	"StykkeNavn"	TEXT,
	PRIMARY KEY("AnsattID","StykkeNavn"),
	FOREIGN KEY("StykkeNavn") REFERENCES "Stykke"("StykkeNavn") ON UPDATE CASCADE,
	FOREIGN KEY("AnsattID") REFERENCES "Medvirkende"("AnsattID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Sal" (
	"Navn"	TEXT,
	--"Område"	TEXT,
	PRIMARY KEY("Navn")
);
CREATE TABLE IF NOT EXISTS "Oppsetning" (
	"OppsetningsID"	INTEGER,
	-- "Navn"	TEXT, 
	"Dato" DATE,
	"Klokkeslett"	TEXT,
	"SalNavn"	TEXT NOT NULL,
	"StykkeNavn"	TEXT NOT NULL,
	PRIMARY KEY("OppsetningsID"),
	FOREIGN KEY("StykkeNavn") REFERENCES "Stykke"("StykkeNavn") ON UPDATE CASCADE,
	FOREIGN KEY("SalNavn") REFERENCES "Sal"("Navn") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Priser" (
	--Endret navn på tabellen til Priser fra Pris
	"OppsetningsID"	INTEGER,
	"Type"	TEXT,
	"Pris"	INTEGER,
	PRIMARY KEY("OppsetningsID","Type"),
	FOREIGN KEY("OppsetningsID") REFERENCES "Oppsetning"("OppsetningsID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Kundeprofil" (
	"KundeID"	INTEGER,
	"TlfNr"	TEXT,
	"Navn"	TEXT,
	"Adresse"	TEXT,
	"Epost"	TEXT,
	PRIMARY KEY("KundeID")
);
CREATE TABLE IF NOT EXISTS "Sete" (
	"StolNr"	INTEGER,
	"RadNr"	INTEGER,
	"Område"	TEXT,
	"SalNavn"	TEXT,
	PRIMARY KEY("StolNr","RadNr","Område","SalNavn"),
	FOREIGN KEY("SalNavn") REFERENCES "Sal"("Navn") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Billett" (
	"StolNr"	INTEGER,
	"RadNr"	INTEGER,
	"Område"	TEXT,
	"OppsetningsID"	INTEGER,
	"KundeID"	INTEGER NOT NULL,
	PRIMARY KEY("StolNr","RadNr","Område","OppsetningsID"),
	FOREIGN KEY("StolNr","RadNr","Område") REFERENCES "Sete"("StolNr","RadNr","Område") ON UPDATE CASCADE,
	FOREIGN KEY("KundeID") REFERENCES "Kundeprofil"("KundeID") ON UPDATE CASCADE,
	FOREIGN KEY("OppsetningsID") REFERENCES "Oppsetning"("OppsetningsID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "BillettTil" (
	"OppsetningsID"	INTEGER,
	"Type"	TEXT,
	"StolNr"	INTEGER,
	"RadNr"	INTEGER,
	"Område"	TEXT,
	PRIMARY KEY("OppsetningsID","Type","StolNr","RadNr","Område"),
	FOREIGN KEY("StolNr","RadNr","Område","OppsetningsID") REFERENCES "Billett"("StolNr","RadNr","Område","OppsetningsID") ON UPDATE CASCADE,
	--FOREIGN KEY("OppsetningsID","Type") REFERENCES "Pris"("OppsetningsID","Type") ON UPDATE CASCADE
	FOREIGN KEY("OppsetningsID","Type") REFERENCES "Priser"("OppsetningsID","Type") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Akt" (
	"AktNummer"	INTEGER,
	"StykkeNavn"	TEXT,
	"AktNavn"	TEXT,
	PRIMARY KEY("AktNummer","StykkeNavn"),
	FOREIGN KEY("StykkeNavn") REFERENCES "Stykke"("StykkeNavn") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Skuespiller" (
	"AnsattID"	INTEGER,
	PRIMARY KEY("AnsattID"),
	FOREIGN KEY("AnsattID") REFERENCES "Ansatte"("AnsattID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "Rolle" (
	"RolleNavn"	TEXT,
	"AnsattID"	INTEGER,
	PRIMARY KEY("RolleNavn","AnsattID"),
	FOREIGN KEY("AnsattID") REFERENCES "Skuespiller"("AnsattID") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "SpillerRolle" (
	"AnsattID"	INTEGER,
	"RolleNavn"	TEXT,
	PRIMARY KEY("AnsattID","RolleNavn"),
	FOREIGN KEY("AnsattID") REFERENCES "Skuespiller"("AnsattID") ON UPDATE CASCADE,
	FOREIGN KEY("RolleNavn") REFERENCES "Rolle"("RolleNavn") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "SpillerIAkt" (
	"AktNummer"	INTEGER,
	"StykkeNavn"	TEXT,
	"OppsetningsID"	INTEGER,
	"AnsattID"	INTEGER,
	"RolleNavn"	TEXT,
	--PRIMARY KEY("AktNummer","StykkeNavn","OppsetningsID"),
	PRIMARY KEY("AktNummer","StykkeNavn","OppsetningsID","AnsattID","RolleNavn"),
	FOREIGN KEY("AnsattID") REFERENCES "Skuespiller"("AnsattID") ON UPDATE CASCADE,
	FOREIGN KEY("OppsetningsID") REFERENCES "Oppsetning"("OppsetningsID") ON UPDATE CASCADE,
	FOREIGN KEY("AnsattID","RolleNavn") REFERENCES "Rolle"("RolleNavn","AnsattID") ON UPDATE CASCADE,
	FOREIGN KEY("AktNummer","StykkeNavn") REFERENCES "Akt"("AktNummer","StykkeNavn") ON UPDATE CASCADE
);
COMMIT;
