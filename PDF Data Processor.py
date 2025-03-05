import PyPDF2

def extract_text_from_pdf(pdf_path, output_txt):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        with open(output_txt, 'w') as txt_file:
            txt_file.write(text)
    print(f"Text saved to {output_txt}!")

# Example usage:
extract_text_from_pdf('input.pdf', 'output.txt')