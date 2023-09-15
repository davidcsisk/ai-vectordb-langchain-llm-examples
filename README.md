# ai-pgvector-langchain-llm-examples
Examples leveraging PostgreSQL PGvector extension, OpenAI / GPT4ALL / etc large language models, and Langchain tying it all together

Example usage:
python demo-pgvector-openai.py
This example application uses OpenAI API for LLM vector embeddings, and PostgreSQL PGvector extension for vector storage and query.
Usage:  demo-pgvector-openai.py -add | -query | -qembed | -sql collection_name 'document_path_and_name'|'question, phrase, or text query'
 Examples:
  add one document:         demo-pgvector-openai.py -add my_collection 'State-of-the-Union-address.txt'
  run query:                demo-pgvector-openai.py -query my_collection 'What statements did the president make about inflation?'
  output pgvector sql:      demo-pgvector-openai.py -sql my_collection 'What statements did the president make about inflation?'
