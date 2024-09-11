SELECT DISTINCT
    Stykke.StykkeNavn,
    Ansatte.Navn,
    Rolle.RolleNavn
FROM
    Stykke
JOIN
    Akt ON Stykke.StykkeNavn = Akt.StykkeNavn
JOIN
    SpillerIAkt ON Akt.AktNummer = SpillerIAkt.AktNummer AND Akt.StykkeNavn = SpillerIAkt.StykkeNavn
JOIN
    Ansatte ON SpillerIAkt.AnsattID = Ansatte.AnsattID
JOIN
    Rolle ON SpillerIAkt.RolleNavn = Rolle.RolleNavn AND SpillerIAkt.AnsattID = Rolle.AnsattID
ORDER BY
    Stykke.StykkeNavn, Ansatte.Navn;

