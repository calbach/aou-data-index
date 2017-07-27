# Curated Data Repository (CDR) Index

## Setup

[Install docker-compose](https://docs.docker.com/compose/install/)

## Run

```
docker-compose up
```

To see the Swagger API definition, open your browser to:

```
http://localhost:9190/v1/ui/
```

## Running tests

```
pip install tox
tox
```

### Useful flags

Support breakpointing with pdb:

```
tox -- -s
```

Run a subset of tests:

```
tox -- -s data_index/test/test_datasets_controller.py:TestDatasetsController
```

## Swagger codegen

```
wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.2/swagger-codegen-cli-2.2.2.jar -O swagger-codegen-cli.jar

java -jar swagger-codegen-cli.jar generate \
  -i api/index.swagger.yaml \
  -l python-flask \
  -DsupportPython2=true,packageName=data_index
```

## Deploy

### Dev

http://bvdp-verily-dev.appspot.com

API push (for changes to api/index.swagger.yaml):

```
gcloud service-management configs list --service=bvdp-verily-dev.appspot.com --project bvdp-verily-dev
```

Update app.yaml with the latest config version:

```
config_id=$(gcloud service-management configs list --service=bvdp-verily-dev.appspot.com --project bvdp-verily-dev --format="csv[no-heading](CONFIG_ID)" --limit 1)
sed -i "s/config_id:.*/config_id: \"${config_id}\"/" app.yaml
```

Backend push:

```
gcloud app deploy --project bvdp-verily-dev
```
