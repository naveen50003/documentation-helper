import os
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.pinecone import Pinecone
from pinecone import Pinecone as PineconeInit

from consts import INDEX_NAME

PineconeInit(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"]
)

def ingest_docs()->None:
    #loader = ReadTheDocsLoader(path='langchain-docs/langchain.readthedocs.io/en/latest', encoding="utf8")
    loader = PyPDFLoader("budget_speech.pdf")
    raw_documents = loader.load()
    print(f"length of the documents --- {len(raw_documents)} before removing few documents")
    #raw_documents = raw_documents[: len(raw_documents) - 600]
    print(f"length of the documents --- {len(raw_documents)} after removing few documents")
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=100, separators=["\n\n","\n"," ",""])
    documents = text_splitter.split_documents(documents=raw_documents)
    #documents = raw_documents
    print(f"Splitted into {len(documents)} chunks")

    # for doc in documents:
    #     old_path = doc.metadata["source"]
    #     new_url = old_path.replace("langchain-docs", "https:/")
    #     doc.metadata.update({"source": new_url})

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("**** Added to Pinecone vectorstore vectors")
   
if __name__ == '__main__':
    ingest_docs()