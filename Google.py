def BW_Google_search(hakusana):
    from googlesearch import search
    for i in search(hakusana, tld ="com", num = 20, stop=20,pause=2):
        print(i)

def BW_Google_search_full(hakusana,maara_tulos):
    from googlesearch import search
    for i in search(hakusana, tld ="com", num = maara_tulos, stop=maara_tulos,pause=2):
        print(i)

def BW_Google_search_tallenta_CSV(hakusana,tiedostonimi):
    haku_tulokset = []
    from googlesearch import search
    for i in search(hakusana, tld ="com", num = 20, stop=20,pause=2):
        haku_tulokset.append(i)

    
    import csv
    def tallenna_csv_tiedostoon(tiedostonimi, data):
        try:
            with open(tiedostonimi, mode='w', newline='') as tiedosto:
                kentat = ['Kentta1']  # Korvaa nämä kenttien nimet omilla tiedoillasi.
                csv_writer = csv.DictWriter(tiedosto, fieldnames=kentat)
                csv_writer.writeheader()
                for rivi in data:
                    csv_writer.writerow(rivi)
            print("Tiedosto tallennettu onnistuneesti.")
        except Exception as e:
            print(f"Virhe tallennettaessa tiedostoa: {e}")

    # Kutsu tallenna_csv_tiedostoon-funktiota ja anna sille tiedostonimi ja haku_tulokset-lista
    #tiedostonimi = 'haku_tulokset_test_99.csv'
    tallenna_csv_tiedostoon(tiedostonimi, haku_tulokset)
    return haku_tulokset

def BW_Google_search_tallenta_CSV(hakusana, tiedostonimi_csv):
    tiedostonimi = tiedostonimi_csv
    try:
        from googlesearch import search
        haku_tulokset = list(search(hakusana, tld="com", num=20, stop=20, pause=2))

        import csv
        def tallenna_csv_tiedostoon(tiedostonimi, data):
            kentat = ['Kentta1']  # Korvaa nämä kenttien nimet omilla tiedoillasi.

            with open(tiedostonimi, mode='w', newline='') as tiedosto:
                csv_writer = csv.DictWriter(tiedosto, fieldnames=kentat)
                csv_writer.writeheader()
                for rivi in data:
                    csv_writer.writerow({'Kentta1': rivi})
            print("Tiedosto tallennettu onnistuneesti.")
        
        # Kutsu tallenna_csv_tiedostoon-funktiota ja anna sille tiedostonimi ja haku_tulokset-lista
        tallenna_csv_tiedostoon(tiedostonimi, haku_tulokset)
    except Exception as e:
        print(f"Virhe hakutulosten hakemisessa tai tallentamisessa: {e}")