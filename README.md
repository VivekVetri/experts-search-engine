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
scrapy crawl expert -o expert.json
```

#Running Backend
```
cd webapp/backend
python3 build_inverted_index.py config.toml
```
