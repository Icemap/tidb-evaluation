# TiDB Evaluation

This is an evaluation dataset build tool for TiDB.

## Prerequisites

- [Python](https://www.python.org/downloads/) version 3.11 or above;
- [Poetry](https://python-poetry.org/);
- Install requirements via `poetry install`

## Usage

### Help Info

```bash
poetry run python main.py --help
```

Example output:

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  save-dataset
```

### Save Dataset

```bash
poetry run python main.py save-dataset
```

Example output:

```
Start to save topics dataset to autoflow_dataset.csv
...
Saved topics dataset to autoflow_dataset.csv
```