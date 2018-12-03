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
```bash
pip3 install -r requirements.txt
python3 tr-engine/etl.py crawler/crawler/expert.json crawler/crawler/cleaned_expert.json
```
