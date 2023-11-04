import PyPDF2

def pdf_to_text(pdf_path, text_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        with open(text_path, 'w') as text_file:
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                text_file.write(text)