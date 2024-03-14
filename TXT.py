def BW_txt_haku12(tiedostonimi, hakusana1,hakusana2 ):
    def hae_tiedostosta(tiedostonimi, hakusana):
        tulokset = []
        try:
            with open(tiedostonimi, 'r', encoding='utf-8') as tiedosto:
                rivit = tiedosto.readlines()
                for indeksi, rivi in enumerate(rivit):
                    if hakusana in rivi:
                        tulokset.append(f"Rivi {indeksi + 1}: {rivi.strip()}")
        except FileNotFoundError:
            print(f"Tiedostoa {tiedostonimi} ei löytynyt.")
        return tulokset

    def toinen_haku(hakutulokset, toinen_hakusana):
        toiset_tulokset = []
        for tulos in hakutulokset:
            if toinen_hakusana in tulos:
                toiset_tulokset.append(tulos)
        return toiset_tulokset


    hakutulokset1 = hae_tiedostosta(tiedostonimi, hakusana1)

    if hakutulokset1:
        #print(f"Ensimmäisen haun tulokset hakusanalle '{hakusana1}':")
        #for tulos in hakutulokset1:
            #print(tulos)



        toiset_tulokset = toinen_haku(hakutulokset1, hakusana2)

        if toiset_tulokset:
            print(f"Toisen haun tulokset hakusanalle '{hakusana2}':")
            for tulos in toiset_tulokset:
                print(tulos)
        else:
            print(f"Ei tuloksia toiselle hakusanalle '{hakusana2}'.")
    else:
        print(f"Ei tuloksia ensimmäiselle hakusanalle '{hakusana1}'.")
    

def BW_pdf_to_txt( pdf_tiedostonimi, txt_tiedostonimi):
    import PyPDF2



    # Avaa PDF-tiedosto binääritilassa
    with open(pdf_tiedostonimi, 'rb') as pdf_tiedosto:
        pdf_reader = PyPDF2.PdfReader(pdf_tiedosto)

        # Tarkista, että PDF-tiedosto on luettavissa
        if len(pdf_reader.pages) > 0:
            # Luo tyhjä tekstitiedosto
            with open(txt_tiedostonimi, 'w', encoding='utf-8') as txt_tiedosto:
                # Käy läpi jokainen sivu ja lisää teksti tekstitiedostoon
                for sivu in pdf_reader.pages:
                    sivun_teksti = sivu.extract_text()
                    txt_tiedosto.write(sivun_teksti)

            print(f'PDF-tiedosto on muunnettu tekstitiedostoksi: {txt_tiedostonimi}')
        else:
            print('PDF-tiedosto on tyhjä tai lukuoikeudet puuttuvat.')
