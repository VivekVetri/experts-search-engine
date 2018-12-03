#Requirements

* python3
* pip3
* mkvirtualenv and workon utilities
* docker

#Setup

```
mkvirtualenv ese-stack
workon ese-stack
pip3 install -r crawler/requirements.txt
pip3 install -r webapp/requirement.txt
pip3 install -r requirements.txt
```

#Online :-
#Running docker containers
```
docker-compose up --build
```

Webapp can be accessed at http://localhost

#Offline :-
#Running Crawler
```
cd crawler/crawler/crawler
scrapy crawl expert -o expert.json
```

#Running Backend
```
cd webapp/backend
python3 build_inverted_index.py config.toml
```

#Running TR-Engine: ETL
* Transforms crawler's raw dataset into MeTA format dataset. Refer Dataset
```bash
pip3 install -r requirements.txt
python3 tr-engine/etl.py crawler/crawler/expert.json tr-engine/experts/expert-queries.csv
```

#Dataset

* experts/experts.dat - contains details of an expert per line
* experts/experts.dat.names - contains name
* experts/experts-queries.txt - contains queries 
* experts/experts-qrels.txt - contains relevance judgements 
* line.toml - format of dataset
* stopwords.txt - stopwords file
