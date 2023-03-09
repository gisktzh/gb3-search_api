# Local Installation
1. Make sure Elasticsearch is running locally
2. Install a Pipenv with the necessary packages by running ```pipenv install```
3. Run the search API with ```pipenv run uvicorn main:gb3_search --reload```

The search API should now listen to http://localhost:8000/. Go to http://localhost:8000/docs to access the API documentation