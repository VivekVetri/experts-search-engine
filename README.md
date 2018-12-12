#Requirements

* python3
* pip3
* mkvirtualenv and workon utilities

#Setup

```
mkvirtualenv ese-stack
workon ese-stack
pip3 install -r requirements.txt
```

#Running Crawler to fetch data
```
cd crawler/crawler
scrapy crawl expert -o expert.json
```

#Running TR-Engine: ETL
* Transforms crawler's raw dataset into MeTA format dataset. Refer Dataset
```bash
python3 tr-engine/etl.py crawler/crawler/expert.json tr-engine/experts/expert-queries.csv
```

#Dataset (tr-engine/experts)

* experts/experts.dat - contains details of an expert per line
* experts/experts.dat.names - contains name
* experts/experts-queries.txt - contains queries 
* experts/experts-qrels.txt - contains relevance judgements 
* line.toml - format of dataset
* stopwords.txt - stopwords file

#Running TR-Engine: Ranker 
```bash
cd tr-engine
python3 ranker.py config.toml bm25
python3 ranker.py config.toml jm 
python3 ranker.py config.toml l2
python3 ranker.py config.toml dp 
```

#Running TR-Engine: Webapp 
```bash
cd tr-engine
python3 webapp.py
```
* You can access the search-engine in http://0.0.0.0:8080

