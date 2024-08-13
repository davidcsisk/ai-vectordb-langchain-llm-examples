# Example of using HuggingFace LLM and Chroma local vector database to customize an LLM with your own data
# python -v venv venv
# venv\Scripts\Activate.ps1
# pip install -U langchain-chroma
# pip install -U langchain-huggingface
# pip install langchain
# pip install langchain-community

import os, sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader

if len(sys.argv) == 1:
   print(f'Usage: {sys.argv[0]} -t(rain) document_path_and_name  | -q(query) "question or search text"')
   quit()

option = sys.argv[1]
#llm_model_name = "all-MiniLM-L6-v2"   # Probably not the best model for this
llm_model_name = "multi-qa-MiniLM-L6-cos-v1"   # Let's try this Q&A model

# You can change the directory name to whatever you desire...in this case, I was having 
# the LLM "read" the Hands-On Machine Learning textbook from my master's in data science. 
# I should extend this to name the dir from the book filename and allow you to specify which book to query
chroma_dir = "./chromadb_data"


if option == '-t':
    filename = sys.argv[2]

    # load the document and split it into chunks
    loader = TextLoader(filename)
    documents = loader.load()

    # split it into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # create the open-source embedding function
    #embedding_function = SentenceTransformerEmbeddings(model_name=llm_model_name)
    embedding_function = HuggingFaceEmbeddings(model_name=llm_model_name)

    # load it into Chroma and save to disk
    db = Chroma.from_documents(docs, embedding_function, persist_directory=chroma_dir)


if option == '-q':

    # create the open-source embedding function
    embedding_function = HuggingFaceEmbeddings(model_name=llm_model_name)

    # load from disk
    db = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)

    # query it
    query = sys.argv[1]
    docs = db.similarity_search_with_score(query)

    # print results
    for doc in docs:
        print(doc)
        