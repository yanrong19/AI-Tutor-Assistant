import os
from langchain_community.document_loaders import PDFPlumberLoader, CSVLoader, UnstructuredHTMLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap = 150
# )

document_loaders = {
    'pdf': PDFPlumberLoader,
    'csv': CSVLoader,
    'html': UnstructuredHTMLLoader
}

knowledge_directory = './uploads'

embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

# Include recrusive text splitter?
def create_vectorstore():
    documents = []

    for knowledge in os.listdir(knowledge_directory):
        try:
            file_path = os.path.join(knowledge_directory, knowledge)
            docs = load_document(file_path)
            documents.extend(docs)
        except Exception as e:
            print(f"Failed to ingest {knowledge}: {e}")
            continue

    if documents:
        #splits = text_splitter.split_documents(documents)
        db = FAISS.from_documents(documents, embeddings)
        return db
    else:
        return None

def load_document(file_path):
    ext = file_path.rsplit(".", 1)[1]
    filename = file_path.rsplit("\\")[-1]

    if ext in document_loaders:
        loader = document_loaders[ext]
        docs = loader(file_path).load()
        return docs
    else:
        print(f'Unidentified extension for: {filename}')
        return []