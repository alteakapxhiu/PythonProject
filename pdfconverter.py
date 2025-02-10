import fitz  

pdf_file = input("Enter the path to the PDF file: ").strip('"')

try:
    pdf_document = fitz.open(pdf_file)
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        
        pix = page.get_pixmap()
        output_file = f"{pdf_file.replace('.pdf', '')}-{page_number + 1}.png"
        
        pix.save(output_file)
        print(f"Saved: {output_file}")
    
    pdf_document.close()
except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
