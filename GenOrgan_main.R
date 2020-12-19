library(httr)
library(jsonlite)
library(hash)

search_fields <- list("title","abstract","keywords","mesh_terms")
keywords <- paste("alk", "lungs", " human", sep = " ")

my_query <- '{
  "size": 10, 
  "from" : 0, 
  "query": {
    "multi_match" : {
      "query" : keywords,
      "fields" : search_fields
    }
  }
}'

my_query <- '{
    "query": {
        "bool" : {
            "must" :[
                {
                    "bool" : {
                        "should" :[
                            {
                                "match" : {"title": "alk"},
                                "match" : {"title": "lungs"}
                                }
                            ]
                        }
                    },
                {
                    "bool" : {
                        "must" :[
                            {
                                "match" : {"title": "human"},
                                "match" : {"title": "Human"}
                                }
                            ]
                        }
                    },
                
                {
                    "bool" : {
                        "should" :[
                            {
                                "match" : {"abstract": "alk"},
                                "match" : {"abstract": "lungs"}
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }'

url_API <- "http://candy.hesge.ch/SIBiLS/MEDLINE/search.jsp"
my_json_query <- fromJSON(my_query)
my_params <- '{"json_query": my_json_query}'
r <- POST(url_API, encode = "json", body = 'my_params')


