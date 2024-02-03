import os
from typing import Any, Dict, List

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores.pinecone import Pinecone
from pinecone import Pinecone as PineconeInit

from consts import INDEX_NAME

PineconeInit(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"]
)

def run_llm(query:str, chat_history: List[Dict[str,any]]) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(temperature=0, verbose=True)
    ## qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)
    qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True)
    return qa.invoke({"question": query, "chat_history": chat_history})

def delete_records() -> bool:
    print("entered delete records")
    pc = PineconeInit()
    index= pc.Index(INDEX_NAME)
    return index.delete(delete_all=True)

if __name__ == "__main__":
    print(run_llm(query="what is RetrievalQA chain?"))