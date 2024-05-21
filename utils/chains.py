import dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

dotenv.load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

def query_llm(query, db):
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
    return qa.invoke(query)