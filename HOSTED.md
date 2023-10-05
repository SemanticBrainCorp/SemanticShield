SemanticShield can be used as an API, either by running server.py independently or by building and running a docker image

For security reasons, this should be hosted on your infrastructure.

## Usage and API


### Semantic Shield

```
curl -X POST http://localhost:8061/shield/v1/check \
-H 'Content-Type: application/json' \
-d '{"text":"was trump a good president?"}'
```

## Response format

```json
{
  "data": {
    "fail": true,
    "fail_data": [
      "political"
    ],
    "fail_type": "TOPIC",
    "message": "I don't like to talk about politics",
    "pii_max": 0,
    "pii_total": 0,
    "replacement_map": null,
    "sanitized": null,
    "usage": 151
  },
  "status": {
    "statusCode": 0,
    "statusDescription": "OK",
    "timestamp": 1696342552
  }
}
```

### Sanitize

```
curl -X POST http://localhost:8061/shield/v1/sanitize \
-H 'Content-Type: application/json' \
-d '{"text":"My name is Jason Bourne"}'
```

## Response format

```json
{
  "data": {
    "fail": true,
    "fail_data": null,
    "fail_type": "PII",
    "message": null,
    "pii_max": 0,
    "pii_total": 0,
    "replacement_map": {
      "Jason Allen": "Jason Bourne"
    },
    "sanitized": "My name is Jason Allen",
    "usage": 0
  },
  "status": {
    "statusCode": 0,
    "statusDescription": "OK",
    "timestamp": 1696342612
  }
}
```

### Revert

```
curl -X POST http://localhost:8061/shield/v1/revert \
-H 'Content-Type: application/json' \
-d '{"text":"My name is Jason Allen", "replacement_map": {"Jason Allen": "Jason Bourne"}}'
```

## Response format

```json
{
  "data": "My name is Jason Bourne",
  "status": {
    "statusCode": 0,
    "statusDescription": "OK",
    "timestamp": 1696342746
  }
}
```


### Configuration

```
curl -X POST http://localhost:8061/shield/v1/sanitize \
-H 'Content-Type: application/json' \
-d '{"text":"My name is Jason Bourne", "config": {"pii": {"use_placeholders": true, "permissive": false}}}'
```

## Response format

```json
{
  "data": {
    "fail": true,
    "fail_data": null,
    "fail_type": "PII",
    "message": null,
    "pii_max": 0,
    "pii_total": 0,
    "replacement_map": {
      "[PERSON 0]": "Jason Bourne"
    },
    "sanitized": "My name is [PERSON 0]",
    "usage": 0
  },
  "status": {
    "statusCode": 0,
    "statusDescription": "OK",
    "timestamp": 1696343778
  }
}
```


## Docker Build
```bash
build.sh
```

## Docker run

Note that Semantic Shield is memory intensive, and you may have to increase the amount of memory available to docker and the container.

Steps to run the docker image:

* create a .env file with your OPENAI key in the format
> OPENAI_API_KEY=sk-....

* run docker compose
> docker-compose up -d

By default the application will run on port 8061, you can change that in the docker-compose.yml file

