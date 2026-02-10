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

#Aggiunta di statistiche
totale_complessivo = sum(totali_prodotti.values())

statistiche = []

for prodotto, totale in totali_prodotti.items():
    media_prezzo = totale / sum(r["quantita"] for r in dati if r["prodotto"] == prodotto)
    percentuale = totale / totale_complessivo
    statistiche.append({
        "prodotto": prodotto,
        "totale": totale,
        "media_prezzo": media_prezzo,
        "percentuale": percentuale
    })

# report csv e json

#csv

# CSV
with open("report_completo.csv", "w", newline="") as f:
    campi = ["prodotto", "totale", "media_prezzo", "percentuale"]
    writer = csv.DictWriter(f, fieldnames=campi)
    writer.writeheader()
    for s in statistiche:
        writer.writerow({
            "prodotto": s["prodotto"],
            "totale": s["totale"],
            "media_prezzo": f"{s['media_prezzo']:.2f}",
            "percentuale": f"{s['percentuale']:.1%}"
        })

# JSON
with open("report_completo.json", "w") as f:
    json.dump(statistiche, f, indent=2)


#stampare a terminale
print("Report generato!")
for prodotto, totale in totali_prodotti.items():
    print(f"{prodotto}: {totale:.2f}")