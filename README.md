# fuzzystrsearch

A simple API to index and match fuzzy data using minhash with adjustable threshold.

## Usage

Install requirements:

`pip3 install -r requirements.txt`

To index values from a file, one line each:

```
./index_data.py ./test.txt
```

Start the API:

```
./app.py
```

Now search something:

```
curl localhost:5000/search?q=hello
```

search with threshold (between 0-1, which is 0% to 100%):

```
curl 'localhost:5000/search?q=hello&threshold=0.1'
```

return any matches (threshold 0):


```
curl 'localhost:5000/search?q=hello&threshold=0'
```

