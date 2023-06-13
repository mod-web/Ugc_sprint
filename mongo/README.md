# Research Results for MongoDB

### To check results

 Raise the claster:
```
docker-compose up --build
```

Set up the cluster:
```
make init
```

### Results
All researches were carried out with the following parameters to reproduce the actual load on DB:
```
Users: 1000
Movies: 100000
Docs: 1000000 (in every collection: likes, bookmarks, reviews)
```

- Average select time for a list of liked movies for 1 user - 3.74 ms
- Average select time for the number of likes for 1 movie - 28.42 ms
- Average select time for a list of bookmarks for 1 user - 3.35 ms
- Average select time for avg numbers of likes for 1 movie - 24.55 ms
- Online insert + select time for 1 document: 0.008 ms

The average time was calculated on the basis of 100 repetitions for each parameter.
