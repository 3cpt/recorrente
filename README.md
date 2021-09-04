# recorrente

[![Scheduled Build](https://github.com/3cpt/recorrente/actions/workflows/schedule.yml/badge.svg)](https://github.com/3cpt/recorrente/actions/workflows/schedule.yml)

A script that gathers information about a user public repositories. 1-time a day
You need to be the owner of the repositories to get the information about views and clones traffic.

## installation

`pip install -r requirements.txt`

## usage

`python3 main.py <GITHUB_TOKEN>`

### github actions

Check this [workflow](.github/workflows/schedule.yml).

## license

[MIT](LICENSE)
