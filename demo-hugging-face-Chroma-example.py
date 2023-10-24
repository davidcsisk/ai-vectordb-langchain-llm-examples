# Example of using HuggingFace LLM and Chroma local vector database to customize an LLM with your own data
# pip install chromadb
# pip install sentence_transformers
# pip install langchain

import os, sys
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

if len(sys.argv) == 1:
   print(f'Usage: {sys.argv[0]} -t(rain) document_path_and_name  | -q(query) "question or search text"')
   quit()

option = sys.argv[1]
llm_model_name = "all-MiniLM-L6-v2"


if option == '-t':
    filename = sys.argv[2]

    # load the document and split it into chunks
    loader = TextLoader(filename)
    documents = loader.load()

    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name=llm_model_name)

    # load it into Chroma and save to disk
    db = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")


if option == '-q':

    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name=llm_model_name)

    # load from disk
    db2 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

    # query it
    query = sys.argv[1]
    docs = db2.similarity_search(query)

    # print results
    print(docs[0].page_content)

