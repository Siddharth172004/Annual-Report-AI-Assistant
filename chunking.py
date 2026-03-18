import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#load_Data
doc = fitz.open("final_dataset.pdf")

documents = []

for page in doc:
    text = page.get_text()
    documents.append(text)

#text chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

text_docs = []
for i,text_page in enumerate(documents):
    chunks = text_splitter.split_text(text_page)
    for chunk in chunks:
        d = Document(page_content= chunk,metadata={"page" : i,"source" : "text"})
        text_docs.append(d)

#Implement OCR (Extract text from images)
ocr_texts = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB",[pix.width, pix.height],pix.samples)
    text = pytesseract.image_to_string(img)

    if text.strip():
        ocr_texts.append(text)
        
image_docs = []
for i,image_page in enumerate(ocr_texts):
    chunks = text_splitter.split_text(image_page)
    for chunk in chunks:
        i = Document(page_content=chunk ,metadata= {"page":i,"source":"image"}) 
        image_docs.append(i)

#Genrate Embedding
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
all_docs = text_docs + image_docs
vectorstore = FAISS.from_documents(all_docs, model)
vectorstore.save_local("Vectordb")