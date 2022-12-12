### Setup

Add a Google Maps API Key in `.env`.

Start the container:

```shell
$ docker compose up
```

Start a shell on the container:

```shell
$ docker compose exec api bash
```

Then in that shell:

```shell
$ poetry run python manage.py migrate
$ poetry run python manage.py runscript insert_branches
```
