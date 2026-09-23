import fitz


def extract_pdf_pages(pdf_file):

    pdf_bytes = pdf_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text("text")

        if text and text.strip():

            pages.append({
                "page": page_number + 1,
                "text": text.strip()
            })

    document.close()

    return pages