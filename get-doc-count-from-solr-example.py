import requests

url = 'http://mrksolr1:8983/solr/mrk-soliant-cand-jobs/query'

payload = {'q':'type:c'}  # Query Solr for type:c

r = requests.post(url, payload)
num_found = r.json()['response']['numFound']
print("type c:", num_found)

payload = {'q':'type:c'}
r = requests.post(url, payload)
num_found = r.json()['response']['numFound']
print("type r:", num_found)
