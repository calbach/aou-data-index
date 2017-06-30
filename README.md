# Curated Data Repository (CDR) Index

## Setup and run

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m data_index
```

To see the Swagger API definition, open your browser to:

```
http://localhost:8080/v1/ui/
```

## Running tests

```
pip install tox
tox
```

## Swagger codegen

```
wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.2/swagger-codegen-cli-2.2.2.jar -O swagger-codegen-cli.jar

java -jar swagger-codegen-cli.jar generate \
  -i api/index.swagger.yaml \
  -l python-flask \
  -DsupportPython2=true,packageName=data_index
```
