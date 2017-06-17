# Curated Data Repository (CDR) Index

## Setup and run

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
(cd src; python -m src/swagger_server)
```

TODO(calbach): docker-compose w/ elastic search. Currently this assumes you have
  an elastic search server already running on port 9200.

To see the Swagger API definition, open your browser to:

```
http://localhost:8080/ui/
```

## Deploy to the dev environment

```
gcloud app deploy --project google.com:bvdp-cdr-index-dev
```

## Swagger codegen

Run via Docker

```
docker run --rm -v ${PWD}/src:/local swaggerapi/swagger-codegen-cli generate -i /local/index.swagger.json -l python-flask -D supportPython2=true -o /local
```
