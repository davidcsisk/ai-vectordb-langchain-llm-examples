import requests

url = 'http://mrksolr1:8983/solr/sisktest1/select'

#payload = {'q':'type:c'}  # Query Solr for type:c

# q=*:*&sort=view_count desc&rows=1&fl=view_count
#http://mrksolr1:8983/solr/sisktest1/select?fl=vid&q=vid:*&rows=1&sort=vid+desc

# When we do this via the fq (filter query), that result is cached before applying the q (query) part
payload = {'fq':'type:c', 'q':'vid:*', 'sort':'vid desc', 'rows':'1', 'fl':'vid'}  # Query Solr for type:c and get max ID for that type
r = requests.post(url, payload)
print(r.json())
maxID = r.json()['response']['docs'][0]['vid']
print('maxID for type c:', maxID)

payload = {'fq':'type:j', 'q':'vid:*', 'sort':'vid desc', 'rows':'1', 'fl':'vid'}  # Query Solr for type:c and get max ID for that type
r = requests.post(url, payload)
print(r.json())
maxID = r.json()['response']['docs'][0]['vid']
print('maxID for type j:', maxID)


# This way may be more clear...query based on type but sort and return the max vid 
payload = {'q':'type:c', 'sort':'vid desc', 'rows':'1', 'fl':'vid'}  # Query Solr for type:c and get max ID for that type
r = requests.post(url, payload)
print(r.json())
maxID = r.json()['response']['docs'][0]['vid']
print('maxID for type c:', maxID)

payload = {'q':'type:j', 'sort':'vid desc', 'rows':'1', 'fl':'vid'}  # Query Solr for type:c and get max ID for that type
r = requests.post(url, payload)
print(r.json())
maxID = r.json()['response']['docs'][0]['vid']
print('maxID for type j:', maxID)
