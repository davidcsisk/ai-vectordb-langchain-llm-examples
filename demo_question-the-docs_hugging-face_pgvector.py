#pip install pgvector
#pip install psycopg2
#pip install langchain
#pip install sentence_transformers
#pip install text_generation


import os, sys
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
#from langchain.document_loaders import TextLoader  this will be deprecated
from langchain_community.document_loaders import TextLoader
# from langchain.docstore.document import Document
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain_community.llms import HuggingFaceTextGenInference

if len(sys.argv) < 4:  # Must pass in 3 arguments
    print("This example cli app uses HuggingFace for LLM vector embeddings, and PostgreSQL PGvector extension for vector storage and query.") 
    print("Usage: ", sys.argv[0], "-add | -query | -qembed | -sql collection_name 'document_path_and_name'|'question, phrase, or text query'")
    print(" Examples:")
    print("  add one document:        ", sys.argv[0], '-add my_collection "US-Constitution-With-Amendments.txt"')
    print("  query & return matches:  ", sys.argv[0], '-query my_collection "What does the constitution say about term limits?"')
    print("  query & return summary:  ", sys.argv[0], '-summary my_collection "What does the constitution say about term limits?"')
    print("  output pgvector sql:     ", sys.argv[0], '-sql my_collection "What does the constitution say about term limits?"')
    quit()


option = sys.argv[1]
COLLECTION_NAME = sys.argv[2]
third_argument = sys.argv[3]

# Set the env variable like so: export CONNECTION_STRING='postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/vector_db'
CONNECTION_STRING = os.getenv('PGVECTOR_CONNECTION')  # This connection string specifies the PostgreSQL database connection.

llm_model_name = "multi-qa-MiniLM-L6-cos-v1"   # Let's try this Q&A model
# model = SentenceTransformer('sentence-transformers/stsb-bert-large')
#llm_model_name = "stsb-bert-large"   # Let's try this Q&A model


# This section allows you to add a document (currently supports only txt files, so convert a PDF or DOCX to text).
# The vector embeddings generated from the content you provide are stored in the vector datastore, which in this case
# is PostgreSQL with the PGvector extension. You are "customizing" the LLM with your own content, and PGvector provides RAG datastore 

if option == '-add':
    # Load the document and split it into chunks
    loader = TextLoader(third_argument)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # create the open-source embedding function
    embedder = SentenceTransformerEmbeddings(model_name=llm_model_name)

    # The PGVector Module will try to create two meta-data tables if they do not already exist, and will add rows with the collection name.
    # Make sure that the collection name is unique and the user has the permission to create a table.
    # If the collection already exists, new documents will be appended.

    db = PGVector.from_documents(
        embedding=embedder,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
    )

    print(f"Document {third_argument} has been 'read', vectorized by the LLM, and stored in the vector storage")


# This section allows you to query the LLM plus your custom content by supplying a search term, full sentence, or anything in between.
# The question text is vectorized using the same LLM that vectorized your content above.  Then PostgreSQL is queried for vector similarity
# between the phrase you entered as a question, and the content that you have stored in Postgres. The -query option returns the query 
# response, while the -sql option allows you to see what type of SQL query is getting issued by Langchain on behalf of the process. The
# SQL statement has the vector embedding values in the query as a sort column. If you take the SQL SELECT statement and run it against the
# database, you should get the exact same output that the Langchain call returns. Note that the score is actually distance, so a smaller
# distance is better...it means a better match.
if option == '-query' or option == '-sql':
    query = third_argument
    # create the embedding function
    embedder = SentenceTransformerEmbeddings(model_name=llm_model_name)
    #embeddings = GPT4AllEmbeddings()
    
    if option == '-sql':    # Output PGvector SQL query with vector embedding, do not execute the query
       query_embedded = embedder.embed_query(query)
       #  SQL query will look something like this: 
       #  SELECT document, (embedding <=> '[-0.020195066928863525, ..., -0.019898081198334694]') as cosine_distance
       #  FROM langchain_pg_embedding ORDER BY cosine_distance LIMIT 3;
       #print(f"SELECT document, (embedding <=> '{query_embedded}') as cosine_dist FROM langchain_pg_embedding ORDER BY cosine_dist LIMIT 3;")
       sql = "SELECT document, (embedding <=> '" + ''.join(str(query_embedded)) + "') as cosine_distance FROM langchain_pg_embedding "
       sql = sql + "ORDER BY cosine_distance LIMIT 3;"
       # NOTE: Above, convert the vector embeddings from a Python list of numbers to a python list of strings, then concatenate the python list  
       # of strings to one long string to then concatenate into the PGvector SQL statement, like so: ...+ ''.join(str(query_embedded)) +... 
       # The commented-out print statement works without all of that, but it only prints the sql statement.
       print(sql)
        
    if option == '-query' or option == '-summary':     # Run the supplied query and return the results or a summary
       db = PGVector(
            collection_name=COLLECTION_NAME,
            connection_string=CONNECTION_STRING,
            embedding_function=embedder,
            distance_strategy = DistanceStrategy.COSINE  # cosine
            #distance_strategy = DistanceStrategy.EUCLIDEAN  # L2
            #distance_strategy = DistanceStrategy.MAX_INNER_PRODUCT  # inner
       )

       # Execute similarity search and get top 3 entries...this vectorizes the query text, then executes a vector distance query in the db
       docs_with_score = db.similarity_search_with_score(query, k=3)

       if option == '-query':
          # Print the vector search results
          for doc, score in docs_with_score:
              print("-" * 80)
              print("Score (aka vector distance...lower is better): ", score)
              print(doc.page_content)
              print("-" * 80)
       
       # It seems that this is quite involved to do with HuggingFace, unless the interface has changed.  Need to go determine that...
       # It looks as though not all HF models support summarizing text.  It might be worth switching this out to GPT4all instead...
       #if option == '-summary':
          # Hand the returned docs to the LLM to summarize, then output the summary
          #llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
          #chain = load_qa_chain(llm, chain_type="stuff")
          