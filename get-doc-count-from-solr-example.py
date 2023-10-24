import requests

url = 'http://solr1:8983/solr/collection1/query'

payload = {'q':'type:c'}  # Query Solr for type:c

r = requests.post(url, payload)
num_found = r.json()['response']['numFound']
print("type c:", num_found)

payload = {'q':'type:c'}
r = requests.post(url, payload)
num_found = r.json()['response']['numFound']
print("type r:", num_found)
