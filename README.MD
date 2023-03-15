# Celery on AWS ECS examples
This repository contains examples with configuration and approaches to successfully run Celery on AWS ECS.

## Running examples
Run examples with docker-compose:
```sh
$ docker-compose up --build -d
```

Open web app [localhost:8004](http://localhost:8004)

You can trigger the jobs by clicking on links.

Check worker logs:
```sh
$ docker-compose logs -f worker
```

Run multiple workers:
```sh
$ export WORKER_REPLICAS=3
$ docker-compose up --build -d
```