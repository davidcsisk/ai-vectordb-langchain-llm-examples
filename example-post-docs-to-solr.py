import requests
import json

# Define the Solr update URL
solr_url = 'http://mrksolr1:8983/solr/sisk-test-1/update'
solr_url_with_commit = f'{solr_url}?commit=true'

# Prepare your JSON-formatted data


data = [
    {
        "id": "1",
        "title": "Document 1",
        "content": "This is the content of document 1."
    },
    {
        "id": "2",
        "title": "Document 2",
        "content": "This is the content of document 2."
    }
]



# Demonstrate updating data & adding fields
# valid field modifiers are:  set (new value to existing field, or add new field), add (to multivalue field), add-distinct, remove, removeregex, inc
data = [
    {
        "id": "1",
        "author": {"set": "Mickey Mouse"}
    },
    {
        "id": "2",
        "author": {"set": "Donald Duck."}
    }
]


# Convert the data to JSON format
json_data = json.dumps(data)

# Set the content type to JSON
headers = {'Content-type': 'application/json'}

# Send a POST request to add documents to Solr
response = requests.post(solr_url_with_commit, data=json_data, headers=headers)

# Check the response
if response.status_code == 200:
    print("Documents added successfully to Solr.")
else:
    print("Failed to add documents to Solr. Status code:", response.status_code)
    print(response.text)

