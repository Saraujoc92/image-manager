# image-manager

Prototype image management service that allows teams to securely store, organize, and retrieve images. Api is served using FastApi to store images in GCS

The app allows _Users_ to upload _Images_. _Users_ belong to _Teams_ and can list _Images_ uploaded by other team members. The api is accessed with api keys provided on user creation. An admin _User_ is created on app initialization. Only this user can create _Teams_. A default api key `ADMIN_ACCESS` is given to this user on the initial database migration. Make sure this key is rotated using `POST /api/v1/user/{user_id}/credentials/rotate`.

## Architecture

This project is meant to hold a collection of applications exposed through an api. This architecture would allow a fast and responsive api delegating long running processes to different applications. This would also allow for independent scaling of the api and the processing apps. These apps would communicate directly, or through other services. For example, events triggered on file upload could trigger a more demanding processing without slowing the user-facing api

```
+-------+                      +-------+
| User  | -------------------->|  API  |
+-------+                      +-------+
                                   |
       +---------------------------+ --------------------------+
       |                           |                           |
+-------------+             +---------------+          +----------------+
|  Databases  |             | Storage Bucket|          | Other services |
+-------------+             +---------------+          +----------------+
       ^                           ^                           ^
       |                           |                           |
       +---------------------------+---------------------------+
                                   |
                        +---------------------+
                        |     App Servers     |
                        |  (1...N Instances)  |
                        +---------------------+
```

The current architecture could be used as a building block of a scalable high demand service enabling scaling of the api service and adding a load balancer.

## Cool features

- Infraestructure defined in terraform for reusable deployments
- Project with full CI/CD integrated through github actions and terraform
  1. runs lint and tests
  2. builds and deploys
  3. runs db migrations
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

- create a `.env` file on the root of the project with the following values

```
PYTHONPATH=SRC

GCLOUD_CREDS_PATH=./gcloud_credentials.json
GOOGLE_CLOUD_PROJECT=********

IMAGE_UPLOAD_BUCKET_NAME=********
```

- To use a local dockerized db, run the migrations before starting the app

```
docker compose up -d
```

- [Activate the environment](#virtual-environment)

```
# still on apps/image_api

DATABASE_URL=postgresql://postgres:password@localhost:5432/image_db alembic upgrade head
```

- local server will be available on `http://localhost:8000/docs`

#### On the local machine

- create a `.env` file on `apps/image_api/src` with the following value, pointing to a bucket on your gcloud project

```
PYTHONPATH=SRC
DATABASE_URL=****
IMAGE_UPLOAD_BUCKET_NAME=****
```

- [Activate the environment](#virtual-environment)
- still on `apps/image_api` run `fastapi dev src/main.py`
- local server will be available on `http://localhost:8000/docs`
