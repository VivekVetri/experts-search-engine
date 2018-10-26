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
python3 crawler/spider.py
scrapy runspider spider.py
```

#Running Backend
```
cd backend
python3 build_inverted_index.py
```
