# Curated Data Repository (CDR) Index

## Setup and run

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
(cd src; python -m src/swagger_server)
```

To see the Swagger API definition, open your browser to:

```
http://localhost:8080/ui/
```

## Swagger codegen

Run via Docker

```
docker run --rm -v ${PWD}/src:/local swaggerapi/swagger-codegen-cli generate -i /local/index.swagger.json -l python-flask -D supportPython2=true -o /local
```
