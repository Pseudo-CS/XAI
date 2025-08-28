import PyPDF2
import docx
import re

class DocumentParser:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path):
        """Extract text from Word document"""
        try:
            doc = docx.Document(docx_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, txt_path):
        """Extract text from plain text file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    
    def parse_document(self, file_path):
        """Main parsing function that handles different file types"""
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self.extract_text_from_docx(file_path)
        elif file_path.lower().endswith('.txt'):
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT.")
    
    def clean_text(self, text):
        """Basic text cleaning"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\.\,\;\:\(\)\-\"]', '', text)
        return text.strip()
