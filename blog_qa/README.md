Run the cli

```bash
modal run api.py --query "your query"
```

Run the api locally

```bash
modal serve api.py 
```

Deploy the api

```bash
modal deploy api.py 
```

Test the api

```bash
curl --get \
  --data-urlencode "query=Your query \
  <url from deploy or serve>
```