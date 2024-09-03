# GB3 Search Backend

The search API for the GB3, serves as an interface for Elasticsearch and realized with Python and FastAPI. test2

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

The image can be run using `docker run`. As a prerequisite, we enforce the use of HTTPS, so the image requires a key and 
a certificate file to be present in the container at `/certs`. The easiest way to achieve this is to mount a volume to 
the container at this location, e.g. using `-v /path/to/certs:/certs`. The latter command would mound the host's 
`/path/to/certs` to the container's `/certs`, assuming the key and certificate files are present in the host's 
`/path/to/certs`.

It also requires the following environment variables to be set:

* `ELASTIC_URL`: Fully-qualified URL to the Elasticsearch URL, e.g. https://localhost:9200
* `ELASTIC_PASSWORD`: The password needed to access Elasticsearch

and, optionally, the name of the key file and/or the certificate file if they are not named `key.pem` and `cert.pem`,:

* `SSL_KEY_FILE`: The name of the key file, defaults to `key.pem`
* `SSL_CERT_FILE`: The name of the certificate file, defaults to `cert.pem`

The container further exposes port `8000`, so a port mapping should be added.

All of these options can be set directly in the docker run command.

An example invocation looks as follows:

```shell
docker run -v /path/to/certs:/certs -p 8001:8000 -e SSL_KEY_FILE=differentname.pem -e ELASTIC_PASSWORD=123 -e ELASTIC_URL=http://localhost:9200 gb3-search-api:latest
```

You can then access https://localhost:8001/docs and verify that the FastAPI client is running. This works even if there
is no backend running, so you can specify any localhost URL and spin up the container to make sure it is working. Note
that there is no non-HTTPS version of the API, so you need to use HTTPS.

## Local Installation

1. Make sure Elasticsearch is running locally
2. Install a Pipenv with the necessary packages by running ```pipenv install```
3. Run the search API with ```pipenv run uvicorn main:gb3_search --reload```

The search API should now listen to http://localhost:8000/. Go to http://localhost:8000/docs to access the API
documentation

### Running Docker container locally

If you need to build the docker container locally, you also need to have the certificates in the `/certs` directory. An
easy way to get a self-signed certificate is to use the [`mkcert` tool](https://github.com/FiloSottile/mkcert).

## Tests

Tests are written using `pytest`.

**Important:** Due to some architectural issues, the tests within `tests/main` cannot be run together. In isolation,
they work well; when all are run together, only once succeeds. This is most likely an issue due to how we're using the
client and how we're injecting elastic search (it gets no calls); so further investigation is needed to determine how we
can reset the mock.