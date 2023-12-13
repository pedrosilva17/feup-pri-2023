#!/bin/bash

#docker run -p 8983:8983 --name meic_solr -v ${PWD}/datasets/generated:/data -d solr:9.3 solr-precreate causes

sleep 15

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/causes/schema

echo "curl done"

# Populate collection using mapped path inside container.

# docker exec -it meic_solr bin/post -c causes /data/sample_semantic.json
docker exec -it meic_solr bin/post -c causes /data/sample.csv

docker cp synonyms.txt meic_solr:/var/solr/data/causes/conf/synonyms.txt
docker cp stopwords.txt meic_solr:/var/solr/data/causes/conf/stopwords.txt

docker restart meic_solr


