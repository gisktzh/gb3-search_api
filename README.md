# GB3 Search Backend

The search API for the GB3, serves as an interface for Elasticsearch and realized with Python and FastAPI.

## Deployment

The search API is deployable with a docker image.

### Dependencies

Requires a running instance of Elasticsearch to run properly.

### Build

Currently, no specific build steps are needed, so a basic docker build command should do the trick:

```shell
docker build -t [name-of-image]:[version] .
# example: docker build -t gb3-search-api:latest .
```

### Run

The image can be run using `docker run`. It requires the following environment variables to be set:

* `ELASTIC_URL`: Fully-qualified URL to the Elasticsearch URL, e.g. https://localhost:9200
* `ELASTIC_PASSWORD`: The password needed to access Elasticsearch

* An option is to specifiy these variables directly in the docker run command.

The container exposes port `8000`, so a port mapping should be added.

An example invocation looks as follows:

```shell
docker run -p 8001:8000 -e ELASTIC_PASSWORD=123 -e ELASTIC_URL=http://localhost:9200 gb3-search-api:latest
```

You can then access http://localhost:8001/docs and verify that the FastAPI client is running. This works even if there
is no backend running, so you can specify any localhost URL and spin up the container to make sure it is working.

## Local Installation

1. Make sure Elasticsearch is running locally
2. Install a Pipenv with the necessary packages by running ```pipenv install```
3. Run the search API with ```pipenv run uvicorn main:gb3_search --reload```

The search API should now listen to http://localhost:8000/. Go to http://localhost:8000/docs to access the API
documentation