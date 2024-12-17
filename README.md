[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit][pre-commit-image]][pre-commit-url]


zurich local map
================

This app was created for the [Airbyte + Motherduck Hackathon](https://airbyte.com/hackathon-airbytemotherduck). It uses Open Government Data (OGD) of the city of Zurich, Switzerland: [Open Data Zurich](https://data.stadt-zuerich.ch/).

## Table of Contents

- [zurich local map](#zurich-local-map)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)

## Installation

* Install python 3.10 e.g. using [pyenv](https://github.com/pyenv/pyenv)
* [Install poetry](https://python-poetry.org/docs/#installation)
* [Install Docker](https://docs.docker.com/get-started/get-docker/)

Run

```
$ mkdir zurich_local && cd zurich_local
$ git clone https://github.com/lukasstolz/zurich_local.git .
$ poetry install
```

## Usage

Create a Motherduck account and database. Copy your access token from the settings.
Create a .env file in the project root and set MD_ACCESS_TOKEN=<your token>

...


[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
[pre-commit-url]: https://github.com/pre-commit/pre-commit
