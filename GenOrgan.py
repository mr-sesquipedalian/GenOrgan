#!/usr/bin/env python
# coding: utf-8

# In[1]:


def genOrgan(gene,organ):
    
    import requests
    import json
    import pandas as pd

    query = {}

    # queries must be formatted in Lucene ElasticSearch style
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html

    # here are different query types :

    # MULTI_MATCH queries
    # use it for searching in specific fields, with a general OR or AND

    search_fields = ["title","abstract","keywords","mesh_terms"]
    # you can use "title^3" for boosting by 3 scores in title
    keywords = gene + " " + organ
    my_operator = "and" # default is "or"
    my_type = "phrase" # use it for phrase matching (exact expression)

    my_query = {
        "size": 10, # maximum amount of hits returned
        "from" : 0, # offset from the first result you want to fetch
        "query": {
            "multi_match" : {
                "query" : keywords,
                "fields" : search_fields
                #,"operator" : my_operator
                #,"type" = "phrase"
                }
            }
    }
    
    # query for required gene and organ
    
    my_query = {
    "query": {
        "bool" : {
            "must" :[ # AND
                {
                    "bool" : {
                        "should" :[ # OR
                            {
                                "match" : {"title": gene},
                                "match" : {"title": organ}
                                }
                            ]
                        }
                    },
                {
                    "bool" : {
                        "should" :[ # OR
                            {
                                "match" : {"abstract": gene},
                                "match" : {"abstract": organ}
                                }
                            ]
                        }
                    },
                ]
            }
        }
    }
    
    # call
    url_API = "http://candy.hesge.ch/SIBiLS/MEDLINE/search.jsp"
    my_json_query = json.dumps(my_query) # json to string
    my_params = {"json_query": my_json_query} # parameters dictionary
    r = requests.post(url = url_API, params = my_params)

    # get response and print in output file
    response = r.text
    with open("SIBiLS_MED_search.json","w",encoding="utf-8") as file:
       file.write(r.text)

    parsed = json.loads(response)
    
    data = []
    for list_item in parsed['hits']:
        source_item = list_item['_source']
        temp_list = [source_item['pmid'], source_item['title'], source_item['abstract']]
        data.append(temp_list)
    
    df = pd.DataFrame(data, columns = ['PMID', 'Title', 'Abstract'])
    return df

