SELECT 
    Stykke.StykkeNavn, 
    Oppsetning.Dato, 
    COUNT(Billett.OppsetningsID) AS AntallSolgtePlasser
FROM 
    Oppsetning 
JOIN 
    Billett ON Oppsetning.OppsetningsID = Billett.OppsetningsID
JOIN
    Stykke ON Oppsetning.StykkeNavn = Stykke.StykkeNavn
GROUP BY 
    Oppsetning.OppsetningsID
ORDER BY 
    AntallSolgtePlasser DESC;
