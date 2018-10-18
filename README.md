#Requirements

* python3
* pip3
* mkvirtualenv and workon utilities

#Setup

```
mkvirtualenv ese-stack
workon ese-stack
pip3 install -r crawler/requirements.txt
python3 crawler/spider.py
scrapy runspider spider.py
```
