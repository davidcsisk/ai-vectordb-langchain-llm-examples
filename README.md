# ai-vectordb-langchain-llm-examples
Examples leveraging PostgreSQL PGvector extension, OpenAI / GPT4ALL / etc large language models, and Langchain tying it all together. (The primary examples are documented below...there are several other examples of various tasks I've had to figure out where documentation was lacking around K-Nearest Neighbor / Vector similarity seach, so feel free to peruse those at your leisure.)

- PGvector (or another vector datastore) provides the "long-term memory" for the vector embeddings generated by customizing the chosen LLM with relevant data/text.
- The LLM itself can be accessed via an API (like OpenAI's GTP3.5-turbo) or a locally installed LLM (like GPT4all's free/open-source downloadable models).
- Langchain is the glue that ties these two together.

The sample command-line applications allow you to hand the LLM a text file or corpus to "read"...those vector embeddings are then stored in PGvector.  (Other vector datastores will be exampled in the future.) You can then query the customized model for ranked matches that provide the answer to the question or search term, or output the PGvector SQL query that is used to execute the vector similarity query (which is useful if you wish to benchmark and compare vector datastore performance and scalability). All sample apps have the built-in command line help similar to below.

The sample application that leverages OpenAI requires you to establish an account with OpenAI...you'll get some minimal account credit that gives you enough room to experiment after you provide them with a credit card number.  Go here for details:  http://www.openai.com

The sample app that leverages GPT4all has no charges (it's free/open-source and downloadable to run locally), but it's also slower since you are likely running it on smaller hardware.  Go here for relevant details: http://gpt4all.io

## Example usage:
Note:  Both demo*.py apps work exactly the same, they just use different LLM's. 

```python demo-pgvector-openai.py
This example application uses OpenAI API for LLM vector embeddings, and PostgreSQL PGvector extension for vector storage and query.
Usage:  demo-pgvector-openai.py -add | -query | -sql collection_name 'document_path_and_name'|'question, phrase, or text query'
 Examples:
  add one document:         demo-pgvector-openai.py -add my_collection 'State-of-the-Union-address.txt'
  run query:                demo-pgvector-openai.py -query my_collection 'What statements did the president make about inflation?'
  output pgvector sql:      demo-pgvector-openai.py -sql my_collection 'What statements did the president make about inflation?'
```
UPATES:  There are now examples and notes around Qdrant (pronounced "quadrant") as a vector DB, plus a couple of examples with Chroma.
