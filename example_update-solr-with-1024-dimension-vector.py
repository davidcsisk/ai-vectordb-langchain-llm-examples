# This script updates solr index to add a field with a 1024 dimension vector

import os, sys
import requests
import json
#import pandas as pd
from sentence_transformers import SentenceTransformer

solr_query_url = 'http://solr1:8983/solr/collection1/query' 
solr_update_url = 'http://solr1:8983/solr/collection1/update?commit=true'

batch_size = 5
start_num = 0

# Instantiate an instance of Bert large LLM...this model returns a 1024 dimension vector
model = SentenceTransformer('sentence-transformers/stsb-bert-large')


# Set the content type to JSON
headers = {'Content-type': 'application/json'}

solr_params = {'q':'*:*', 'fl':'id, title', 'sort':'id asc', 'rows':batch_size, 'start':start_num}

solr_response = requests.post(solr_query_url, solr_params)

#print(solr_response.json())

#solr_rows = json.loads(solr_response.json()['response']['docs'])  # Parse the json so we can work with it in bulk
solr_rows = solr_response.json()['response']['docs']  # Parse the json so we can work with it in bulk
#print(solr_rows)

# Split the id's and titles out to separate lists...the titles will be passed into the model to calculate vector embeddings
id_list = [entry['id'] for entry in solr_rows]
title_list = [entry['title'] for entry in solr_rows]

# Pass in the list of title's and catch the returned vector embeddings
vector_embeddings = model.encode(title_list)

# Assemble the json doc for the update call to Solr
data_to_update = []
for id, vector in zip(id_list, vector_embeddings):
    entry = {"id": id, "vector1024": {"set": vector.tolist()}}
    data_to_update.append(entry)

# Convert the list of dictionaries to JSON
json_data = json.dumps(data_to_update)

# Send a POST request to add documents to Solr
response = requests.post(solr_update_url, data=json_data, headers=headers)

print(response)

   
   


