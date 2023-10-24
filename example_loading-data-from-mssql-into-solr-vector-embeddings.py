# This script does the following:
# 1) Queries ATS to get a batch of job data and stores it in a dataframe
# 2) Calls the candidate/job matching model API with the batch of rows
# 3) Stores the vector embedding results from the API in a dataframe
# 4) Outputs the final data as JSON posted to Solr

# This calls our dev AzuleML endpoint with candidate or job data, and catches the vector data returned by the model
#POST http://52.151.224.249:80/api/v1/service/futuresearch-embedding/score
#inputdata = {"data": [{"id": 0, "text": "Financial Controller"}, 
#          {"id": 1, "text": "Vice President of Personal Finance"}]}
# The API call can accept up to 500 records per call.
# Output is id, title, and 32 dimension vector embedding.

# Job query:       select top 500 jobPostingID, title from bullhorn1.BH_JobOpportunity where title is not null order by 1;

import requests
import os, sys
import json
import pandas as pd
from sqlalchemy import create_engine #Note: Latest SQLalchemy2.x will not work with Pandas 1.5.x
import datetime


# URL for the vector embedding API call
model_url = 'http://52.151.224.249:80/api/v1/service/futuresearch-embedding/score'

# Solr POST url
#solr_url = 'http://mrksolr1.bos.bullhorn.com:8983/solr/sisk-test-1/update'
solr_url = 'http://mrksolr1.bos.bullhorn.com:8983/solr/soliant-jobs/update'
#solr_url = 'http://devsolr1.dev.bullhorn.com:8983/solr/sisk-test-collection/update'

# For posting documents to Solr, set the content type to JSON
solr_headers = {'Content-type': 'application/json'}

# Add the commit parameter to the URL to enable auto-commit
solr_url_with_commit = f'{solr_url}?commit=true'

# Read the connection info from a conn file in the script directory, and open a connection to SQLServer
connfile = 'mssql.conn'
with open(connfile) as f:
    conninfo = f.read()
engine_mssql = create_engine(conninfo, encoding='utf16', execution_options={"isolation_level": "READ UNCOMMITTED"})

# File that tracks last ID loaded to Solr
last_id_file = 'state-jobs-last-id.cfg'

# Check that the lastID file already exists...if not, create it and set the lastID to 0 
if os.path.exists(last_id_file) == False: 
    with open(last_id_file, 'w') as f:
        f.write('0')

with open(last_id_file) as f:
    last_id = f.read()

print(f"{datetime.datetime.now()}: {sys.argv[0]} Starting executing with lastID {last_id}...")

row_count = 1 # Set this to an artificial value to get into the first pass of the loop

while row_count > 0: 
    # Get the last known last ID processed
    with open(last_id_file) as f:
        last_id = f.read()

    job_query_sql = 'select top 500 jobPostingID id, title text from bullhorn1.BH_JobOpportunity \
                     where title is not null and jobPostingID > ' + last_id + 'order by 1;'
    df_jobdata = pd.read_sql(job_query_sql, engine_mssql)
    row_count = df_jobdata.shape[0]
    if row_count > 0:
        last_id = str(df_jobdata['id'].tail(1).item())
    else:
        break

    # Output the batch of rows to a dictionary, then wrap the dict in another dict to get the right JSON format for the API call
    dict_jobdata = df_jobdata.to_dict('records')
    inputdata = {'data': dict_jobdata }   # Nest the DF inside another JSON document so it looks like our sample input data

    # Make the API call
    response = requests.post(model_url, json = inputdata)

    # Check if the call succeeded
    #print('RESPONSE: ', response.status_code) # Should be 200
    #print(json.dumps(response.json(), indent=2))  # Print readable structured json

    # Put the json into a dictionary
    response_dict = response.json()

    # Make a dataframe from the output section of the dictionary
    df_jobvectors = pd.DataFrame(response_dict['output'])
    # Set column names to "title" and "vector"...we've already created a vector field with 32 dimensions and datatype DenseVectorField
    df_jobvectors = df_jobvectors.rename({'text':'title', 'embedding':'vector'}, axis='columns')  # Should now have id, title, vector
    #print(df_jobvectors)

    data_payload = df_jobvectors.to_json(orient='records')
    
    #print("Sent: ", data_payload)
    add_docs = requests.post(solr_url_with_commit, data=data_payload, headers=solr_headers)
    #print("Response: ", add_docs.json())
    print(f"{datetime.datetime.now()}: {sys.argv[0]} Last ID: {last_id}")
    #print(".", end="")

    with open(last_id_file, 'w') as f:
        f.write(last_id)
    
print(f"{datetime.datetime.now()}: {sys.argv[0]} \nFinished executing...")
