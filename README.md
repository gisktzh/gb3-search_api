# Local Installation
1. Install Elasticsearch and Kibana using ```docker compose up``` in this folder
2. Import the index for addresses to Elasticsearch with FME by running FME/address_index.fmw (connect to PostGIS database)
3. Install a Pipenv with the necessary packages by running ```pipenv install```
4. Run the search API with ```pipenv run uvicorn main:gb3_search --reload```

The search API should now listen to http://localhost:8000/. Go to http://localhost:8000/docs to access the API documentation