import csv
import json
import os

#input: puoi cambiare filename
filename = "ventide.csv" # o "vendite.json"

dati = []

#determinare il tipo di file e leggere i dati

if filename.endswith(".csv"):
    with open(filename, newline="") as f:
        lettore = csv.DictReader(f)
        for riga in lettore:
            dati.append({
                "prodotto":riga["prodotto"],
                "quantita":int(riga["quantita"]),
                "prezzo":riga["prezzo"]
            })
elif filename.endswith(".json"):
    with open(filename) as f:
        json_dati = json.load(f)
        for riga in json_dati:
            dati.append({
                "prodotto": riga["prodotto"],
                "quantita": riga["quantita"],
                "prezzo": riga["prezzo"] 
            })
else:
    raise ValueError("Formato file non supportato")

#calcolo del totale per ogni prodotto

totali_prodotti = {}

for riga in dati:
    prodotto = riga["prodotto"]
    totale_riga = riga["quantita"] * riga["prezzo"]

    if prodotto in totali_prodotti:
        totali_prodotti[prodotto] += totale_riga
    else:
        totali_prodotti[prodotto] = totale_riga

# report csv e json

#csv

with open("report.csv", "w", newline="") as f:
    campi=["prodotto","totale"]
    writer = csv.DictWriter(f, fieldnames=campi)
    writer.writeheader()
    for prodotto,totale in totali_prodotti.items():
        writer.writerow({"prodotto":prodotto, "totale":totale})

#json
report_json = [{"prodotto": p, "totale": t} for p,t in totali_prodotti.items()]

with open("report.json", "w") as f:
    json.dump(report_json, indent=2)


#stampare a terminale
print("Report generato!")
for prodotto, totale in totali_prodotti.items():
    print(f"{prodotto}: {totale:.2f}")