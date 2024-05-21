import os
from langchain_community.document_loaders import PDFPlumberLoader, CSVLoader, UnstructuredHTMLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

document_loaders = {
    'pdf': PDFPlumberLoader,
    'csv': CSVLoader,
    'html': UnstructuredHTMLLoader
}

embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

# Include recrusive text splitter?
def create_vectorstore():
    knowledge_directory = './uploads'
    documents = []

    for knowledge in os.listdir(knowledge_directory):
        file_path = os.path.join(knowledge_directory, knowledge)
        docs = load_document(file_path)
        documents.extend(docs)

    if documents:
        db = FAISS.from_documents(documents, embeddings)
        return db
    else:
        return None

def load_document(file_path):
    ext = file_path.rsplit(".", 1)[1]
    filename = file_path.rsplit("\\")[-1]

    if ext in document_loaders:
        try:
            loader = document_loaders[ext]
            docs = loader(file_path).load()
            return docs
        except:
            print(f'error loading document: {filename}')
    else:
        print(f'Unidentified extension for: {filename}')
        return []