# ==========================*- R & Python -*==============================#
# # _  _ _      South       |                                                
# #| |/ / |     China       | Project: Rename Pdf Files as papers title         
# #| ' /| |     University  | Author: John Kong                              
# #| . \| |___  Of          | Date: 2024-12-16                      
# #|_|\_\_____| Technology  |                                                  
# ========================================================================#

from PyPDF2 import PdfReader
import re
import os

def extract_title_from_pdf(pdf_path):
    """Extract paper titles from metadata or content of PDF files"""
    try:
        reader = PdfReader(pdf_path)
        # Retrieve the title from the metadata (if any)
        meta = reader.metadata
        title = meta.title
        if meta.subject:
            title = title+"_"+str(meta.subject)
            title = title.split("doi:")[0]
            title = re.sub(r'[\/:*?"<>|]', '', title)
        else:
            title = title
        if not title:  
          # If there is no title in the metadata(Just Like Physics of Fluids), try extracting from the first page
            first_page = reader.pages[1]
            text = first_page.extract_text()
          # Using regular expressions to match titles
            title_match = re.search(r'^[A-Za-z0-9\s\(\)\-:,.]+', text)
            if title_match:
                title = title_match.group(0).strip()
                title = title_match.group(0).replace('\n', ' ')
          # Remove illegal characters in the title
                title = re.sub(r'[\/:*?"<>|]', '', title)
            else:
                title = "Untitled"
        return title
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return "Untitled"


def rename_pdfs():
    """Traverse the current directory and rename all PDF files"""
    current_dir = os.getcwd()  
    for filename in os.listdir(current_dir):
        if filename.lower().endswith('.pdf'):
            old_pdf_path = os.path.join(current_dir, filename)
            title = extract_title_from_pdf(old_pdf_path)
            new_filename = f"{title}.pdf"
            new_pdf_path = os.path.join(current_dir, new_filename)
            try:
                os.rename(old_pdf_path, new_pdf_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Error renaming {filename}: {e}")


# Run the script
rename_pdfs()
