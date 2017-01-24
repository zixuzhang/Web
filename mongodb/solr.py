#-*- coding: utf-8 -*-
import solr

# create a connection to a solr server
s = solr.SolrConnection('http://127.0.0.1:8083/solr')

# add a document to the index
doc = dict(
    id=1,
    title='Lucene in Action',
    author=['Erik Hatcher', 'Otis Gospodnetić'],
    )
s.add(doc, commit=True)

# do a search
response = s.select('title:lucene')
for hit in response.results:
    print hit['title']