### 1)Run DOCKER:
```
sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
```

### 2)RUN MongoDB:
```
mongod -f /etc/mongod.conf
```

### 3)CROWL
```
scrapy crawl elektronik_bestellers
scrapy crawl elektronik_bestellers -o products.csv
scrapy crawl elektronik_bestellers -a act=dowland
```
