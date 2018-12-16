# Goal

The goal of the **Expert Search Engine** is to create a tool that is both accurate and user friendly. Given a query, the engine will list all the experts along with important information about them. Most researchers have home pages in their university websites. The strategy of the expert search engine is to use the home pages of the researchers to build the document collection. We will start with experts in Computer Science in the top colleges of the US.


# Requirements

* python3
* pip3
* mkvirtualenv and workon utilities (optional)

# Setup

```
mkvirtualenv ese-stack
workon ese-stack
pip3 install -r requirements.txt
```

# Usage

## Running Crawler to fetch data
```
cd crawler/crawler
scrapy crawl expert -o expert.json
```
* *Note:* This will take sometime to download the data. We have added 'crawler/crawler/expert.json' to save time.

## Running TR-Engine: ETL
* Transforms crawler's raw dataset (expert.json) into MeTA format dataset. Refer Dataset topic below.
```bash
python3 tr-engine/etl.py crawler/crawler/expert.json tr-engine/experts/experts-rel-judgements.csv
```

## Dataset (tr-engine/experts)

* experts/experts.dat - contains details of an expert per line
* experts/experts.dat.names - contains name
* experts/experts-queries.txt - contains queries 
* experts/experts-qrels.txt - contains relevance judgements 
* line.toml - format of dataset (static file)
* stopwords.txt - stopwords file (static file)
* experts-rel-judgements.csv - Relevance judgements mapping (manually prepared static file)

## Running TR-Engine: Ranker Batch
```bash
cd tr-engine
python3 ranker.py config.toml bm25
python3 ranker.py config.toml jm 
python3 ranker.py config.toml l2
python3 ranker.py config.toml dp 
```

## Running TR-Engine: Webapp 
```bash
cd tr-engine
python3 webapp.py
```
* You can access the search-engine in http://0.0.0.0:8080
* Sample queries to try - "computer graphics", "cryptography", "computer networks", "genomics", "machine learning"
