import dotenv
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from utils.prompt_templates import GENERAL_TUTOR_PROMPT

dotenv.load_dotenv()

METADATA_ATT ={
    'pdf': ['page']
}

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# Augmented Generation
def query_llm(query, db):
    chain = GENERAL_TUTOR_PROMPT | llm
    response = chain.invoke(
        {
            "context": extract_k_docs(query, db, 3),
            "input": query,
        }
    )
    return response

# Retrieval
def extract_k_docs(query, db, k):
    extracted_docs = []
    try:
        #Metadata filering for future features (which docs to extract information from)
        docs = db.similarity_search(query=query, k=k)
        for doc in docs:
            try:
                metadata = doc.metadata
                file_name, ext = metadata['source'].rsplit('\\')[-1].split(".")
                filtered_metadata = {key: metadata[key] for key in METADATA_ATT[ext] if key in metadata}
                filtered_metadata['file_name'] = file_name
                d = Document(page_content=doc.page_content, metadata=filtered_metadata)
                extracted_docs.append(d)
            except Exception as e:
                print(f'Error extracting {doc}: {e}')
                continue
        print(extracted_docs)
        return extracted_docs
    except Exception as e:
        print(f"Error with vectorstore for extraction: {e}")
        return []