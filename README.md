# recorrente

[![Scheduled Build](https://github.com/3cpt/recorrente/actions/workflows/schedule.yml/badge.svg)](https://github.com/3cpt/recorrente/actions/workflows/schedule.yml)

A script that gathers information about a user public repositories. Best use is 1-time a day because it always gather the information about the last day (now - 1).
You need to be the owner of the repositories to get the information about views and clones traffic.

## installation

`pip install -r requirements.txt`

## usage

```
usage: main.py [-h] [--fork] [--path PATH] token

positional arguments:
  token        github token

optional arguments:
  -h, --help   show this help message and exit
  --fork       include forks
  --path PATH  file path
```

### github actions

Check this [workflow](.github/workflows/schedule.yml). Executes the script and upload the `csv` to the repository.

## license

[MIT](LICENSE)
