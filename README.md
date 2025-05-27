# image-manager

Prototype image management service that allows teams to securely store, organize, and  retrieve images. Api is served using FastApi to store images in GCS

## Architecture

This project is meant to hold a collection of applications exposed through an api. This architecture would allow a fast and responsive api 
delegating long running processes to different applications. This would also allow for independent scaling of the api and the processing apps.

```
+-------+        +-------+
| User  | -----> |  API  |
+-------+        +-------+
                     |
       +-------------+-------------+
       |                           |
+------------+             +---------------+
|  Database  |             | Storage Bucket|
+------------+             +---------------+
       ^                           ^
       |                           |
       +-------------+-------------+
                     |
          +---------------------+
          |     App Servers     |
          |  (1...N Instances)  |
          +---------------------+
```

## Cool features

- Infraestructure defined in terraform for reusable deployments
- Project with full CI/CD integrated through github actions and terraform
- Configurable logs bucket to store important events


## Api docs

A demo of this API can be found [here](https://image-manager-api-2anky2ruiq-ew.a.run.app/docs)

## Development

This project uses [uv](https://docs.astral.sh/uv/) as a package manager


### Virtual Environment

On the fastapi app directory install the dependencies and activate the environment
```
cd apps/image_api
uv sync
source .venv/bin/activate
```

### Run api tests

```
export PYTHONPATH=./src
pytest
```

### Run locally

#### Prerequisites

- `gcloud_credentials.json` file should be present on the root of the project
- Set up [Google Application Default Credentials](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
- Create a project and a gcs bucket to upload images

#### Using docker

From the root folder run 

- create a `.env` file on the root of the project with the following values
```
PYTHONPATH=SRC

GCLOUD_CREDS_PATH=./gcloud_credentials.json
GOOGLE_CLOUD_PROJECT=********

IMAGE_UPLOAD_BUCKET_NAME=********
```
- run `docker compose up`
- local server will be available on `http://localhost:8000/docs`

#### On the local machine

- create a `.env` file on `apps/image_api/src` with the following value, pointing to a bucket on your gcloud project
```
PYTHONPATH=SRC
DATABASE_URL=****
IMAGE_UPLOAD_BUCKET_NAME=****
``` 
- `cd apps/image_api`
- [Activate the environment](#virtual-environment)
- run `fastapi dev src/main.py`
- local server will be available on `http://localhost:8000/docs`

