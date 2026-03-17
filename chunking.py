import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

doc = fitz.open("final_dataset.pdf")

text_data = []

for page in doc:
    text = page.get_text()
    text_data.append(text)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = text_splitter.split_text("\n".join(text_data))
documents = [Document(page_content=chunk) for chunk in chunks]

model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embed = FAISS.from_documents(documents,model)
embed.save_local("Vectordb/text_index")

# os.makedirs("images",exist_ok = True)

# image_paths = []

# for page_index in range(len(doc)):

#     page = doc[page_index]

#     images = page.get_images(full=True)

#     for img_index, img in enumerate(images):

#         xref = img[0]

#         base_image = doc.extract_image(xref)

#         image_bytes = base_image["image"]
#         # image size check
#         width = base_image["width"]
#         height = base_image["height"]

#         # small images skip
#         if width < 400 or height < 400:
#             continue

#         image_path = f"images/page{page_index}_{img_index}.png"

#         with open(image_path, "wb") as f:
#             f.write(image_bytes)

#         image_paths.append(image_path)

# ocr_texts = []

# for path in image_paths:

#     image = Image.open(path)

#     text = pytesseract.image_to_string(image)

#     # whitespace remove
#     text = text.strip()

#     # meaningful text check
#     if len(text) > 20:
#         ocr_texts.append(text)

ocr_texts = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB",[pix.width, pix.height],pix.samples)
    text = pytesseract.image_to_string(img)

    if text.strip():
        ocr_texts.append(text)

image_docs = [Document(page_content=t) for t in ocr_texts]

image_vectorstore = FAISS.from_documents(image_docs, model)

image_vectorstore.save_local("Vectordb/image_index")