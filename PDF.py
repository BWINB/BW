def BW_PDF_all_merge(merge_pdf_name):
    import os
    from PyPDF2 import PdfMerger

    x = [a for a in os.listdir() if a.endswith(".pdf")]

    merger = PdfMerger()

    for pdf in x:
        merger.append(open(pdf, 'rb'))


    merger.write(merge_pdf_name)
    merger.close()


def BW_PDF_remove_encryption_all_for():
    import os
    import pikepdf


    x = [a for a in os.listdir() if a.endswith(".pdf")]
    for pdf in x:
        pdf_a = pikepdf.open(pdf, allow_overwriting_input=True)
        new_pdf_filename = pdf
        pdf_a.save(new_pdf_filename)



import os

from PyPDF4.pdf import PdfFileReader, PdfFileWriter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def create_page_pdf(num, tmp):
    c = canvas.Canvas(tmp)
    for i in range(0, num + 1):
        c.drawString((210 // 2) * mm, (4) * mm, str(i))
        c.showPage()
    c.save()


def add_page_numgers(pdf_path):
    """
    Add page numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    """
    tmp = "__tmp.pdf"

    writer = PdfFileWriter()
    with open(pdf_path, "rb") as f:
        reader = PdfFileReader(f, strict=False)
        n = reader.getNumPages()

        # create new PDF with page numbers
        create_page_pdf(n, tmp)

        with open(tmp, "rb") as ftmp:
            number_pdf = PdfFileReader(ftmp)
            # iterarte pages
            for p in range(n):
                page = reader.getPage(p)
                numberLayer = number_pdf.getPage(p)
                # merge number page with actual page
                page.mergePage(numberLayer)
                writer.addPage(page)

            # write result
            if writer.getNumPages():
                newpath = pdf_path[:-4] + "_sivu.pdf"
                with open(newpath, "wb") as f:
                    writer.write(f)
        os.remove(tmp)


def PDF_merge_table_content_page(header_name,PDF_name):
    import csv
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from pikepdf import Pdf, OutlineItem



    from glob import glob




    output_pdf = "0001_Sisällysluettelo.pdf"
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)


    styles = getSampleStyleSheet()


    title = Paragraph("<b>{}</b>".format(header_name), styles['Title'])

    content = [title]

    content.append( Spacer(1, 12))
    content.append(Paragraph("<b>Sisällysluettelo:</b>", styles['Normal']))

    page_count = 1
    pdf = Pdf.new()
    with pdf.open_outline() as outline:
         for file in glob('*.pdf'):
            src = Pdf.open(file)
            oi = OutlineItem(file, page_count)
            #outline.root.append(oi)

            string_T = "...."
            tiedoston_nimi = file
            #tiedoston_polku = row["Tiedoston polku"]
            subtitle_text = "<i> {} ....{}</i>".format(tiedoston_nimi[0:-4],page_count)
            #subtitle_text = "<i> {} ................................{}.................................................{}</i>".format(tiedoston_nimi[3:-4],string_T*((int(30-len(tiedoston_nimi)))),page_count)
            subtitle = Paragraph(subtitle_text, styles['Normal'])
            content.append(subtitle)
            #content.append(PageBreak())
            page_count += len(src.pages)

    content.append(PageBreak())


    doc.build(content)

    print(f"Uusi PDF-tiedosto '{output_pdf}' on luotu.")

    pdf = Pdf.new()

    page_count = 0

    with pdf.open_outline() as outline:
         for file in glob('*.pdf'):
            src = Pdf.open(file)
            oi = OutlineItem(file, page_count)
            outline.root.append(oi)
            page_count += len(src.pages)
            pdf.pages.extend(src.pages)


    pdf.save(PDF_name)
    add_page_numgers(PDF_name)




def PDF_rename(dir_str, name_start, name_end):
    import os
    directory = dir_str
    # Haetaan kaikki kansiossa olevat tiedostot
    for filename in os.listdir(directory):
        # Tarkistetaan onko tiedosto pdf
        if filename.endswith('.pdf'):
            # Poistetaan .pdf tiedostonimestä
            base_name = filename[:-4]
            # Muodostetaan uusi nimi
            new_name = name_start + "_" + base_name + name_end + ".pdf"
            # Muodostetaan polut vanhalle ja uudelle nimelle
            original_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            # Nimetään tiedosto uudelleen
            os.rename(original_path, new_path)
            #print(f'Renamed {filename} to {new_name}')

def split_pdf_into_pages(pdf_path):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        new_page_pdf_path = f"{pdf_path[:-4]}_page_{page_num + 1}.pdf"
        new_doc.save(new_page_pdf_path)
        new_doc.close()

    doc.close()
import os
import shutil

def rename_and_move_pdfs(root_dir, destination_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                old_path = os.path.join(root, file)
                dir_path = os.path.relpath(root, root_dir)
                juurikansio_nimi = os.path.basename(root_dir)
                new_name = f"{juurikansio_nimi}_{dir_path}_{file}"
                new_path = os.path.join(destination_dir, new_name)
                
                try:
                    # Kopioi alkuperäinen tiedosto ja muuta nimi
                    shutil.copy2(old_path, new_path)
                    print(f"Kopioitu ja nimetty uudelleen: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Virhe tiedostoa '{old_path}' kopioitaessa ja nimettäessä: {e}")


import os
from PyPDF2 import PdfMerger

def merge_pdfs_in_folders_new(name):
    # Luo PDF-tiedostojen yhdistäjä
    merger = PdfMerger()

    # Hae nykyisen kansion kaikki alikansiot ja niiden sisältämät .pdf-tiedostot
    for root, _, files in os.walk("."):
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]

        # Jos kansiossa on .pdf-tiedostoja, lisää ne yhdistäjään
        if pdf_files:
            for pdf_file in pdf_files:
                pdf_path = os.path.join(root, pdf_file)
                merger.append(pdf_path)

    # Yhdistä tiedostot ja tallenna yhteenlaitto.pdf
    merger.write(name)
    merger.close()