# Car price prediction

This is a course project for Machine Learning Beginning course from [Projector](https://prjctr.com/). 

Consist of containers for data collection and processing, notebook for models training and web server for models evaluation.

## Requirements

For the data collection, data processing and web server:
 - [Docker](https://docs.docker.com/get-docker/)
 - [Docker Compose](https://docs.docker.com/compose/install/)
 - [PostgreSQL database](https://www.postgresql.org/download/) (can be local and added to docker compose or could be in cloud)

For the models training:
 - [Python 3.10](https://www.python.org/downloads/release/python-3100/)
 - [Jupyter Notebook](https://jupyter.org/install)

## Setup

After cloning repository, you need to create `.env` file in the root of the project with next content:
```env
SQLALCHEMY_DATABASE_URL=postgresql://user:password@host:port/database-name
PROVINCE=BC
SECRET_KEY=django-secret-key
DB_NAME=database-name
DB_HOST=host
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
```

Where `PROVINCE` is optional configuration for data collection script that defines province for which data will be collected.
It's two capital letter codes of Canadian provinces.

After that you need to build containers with next command:
```bash
docker-compose build 
```

## Data collection

For data collection you need to run `scrapper` container:
```bash
docker-compose up -d scrapper
```

It will collect data from [autotrader](https://www.autotrader.ca/) and save it to the database. Depending on the `PROVINCE` configuration it would be downloading data for single province or from the whole country until all data will be collected.
After finishing data collection, container will be stopped automatically and do not restart.

## Data processing

For data processing you need to run `cleaner` container:
```bash
docker-compose run cleaner
```

you will enter container with bash, and you need to run next command with several options to process data:
```bash
python data/processing.py --mode <mode> --batch-size <batch-size>
```

where:
 - `mode` - mode of processing, could be `clean`, `fill` and `all`, where `clean` will clean listings data, `fill` will fill other models like Provinces, Cities, Makers, Models and `all` will do both. Default is `clean`
 - `batch-size` - int value of batch size for processing, default is 100

## Models training

For models training you need to run jupyter notebook, open [notebook](src/data/ml/gym.ipynb) and follow instructions in it. Models would be saved and then you can upload them into web server trough default Django admin panel.


## Web server

For web server you need to run `web` container:
```bash
docker-compose up -d web
```

web server will be available on `localhost:8000` and links for the prediction pages would be:
 - http://localhost:8000/cars/car-listing-prediction/ - for manually adding full car details and getting prediction
 - http://localhost:8000/cars/url-prediction/ - for prediction by autotrader listing url

and admin panel would be available on http://localhost:8000/admin/. You can create superuser inside a container to access it:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Troubleshooting

Logs of the containers can be viewed with next command:
```bash
docker-compose logs -tf NAME_OF_CONTAINER_FROM_DOCKER_COMPOSE_YAML
```