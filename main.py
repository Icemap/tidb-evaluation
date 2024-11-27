import json
import os

import click
from dotenv import load_dotenv
from tqdm import tqdm

from asktug import get_topics
from classification import classify
from output import to_classification_csv

load_dotenv()


@click.group(context_settings={'max_content_width': 150})
def cli():
    pass


@cli.command()
@click.option('--output', '-o', default='autoflow_dataset.csv', help="Output file, default=autoflow_dataset.csv")
@click.option('--file_type', '-t', default="autoflow",
              help="Output format, default=autoflow, options=[jsonl, autoflow]")
@click.option('--category-size', '-s', default=100, help="Size of each category, default=100")
def save_dataset(output, file_type, category_size):
    # When it's called, the command name is "save-dataset"

    from output import to_jsonl, to_autoflow_eval_dataset
    print(f"Start to save topics dataset to {output}")

    topics = get_topics(max_topics_per_category=category_size)
    if file_type == "jsonl":
        to_jsonl(topics, output)
    elif file_type == "autoflow":
        to_autoflow_eval_dataset(topics, output)
    else:
        raise ValueError(f"Invalid output format: {file_type}")

    print(f"Saved topics dataset to {output}")


@cli.command()
@click.option('--csv', default='autoflow_dataset.csv', help="Output file, default=autoflow_dataset.csv")
@click.option('--output', '-o', default='autoflow_dataset_type.csv', help="Output file, default=autoflow_dataset_type.csv")
@click.option('--category-size', '-s', default=100, help="Size of each category, default=100")
def classify_csv(csv, output, category_size):
    import pandas as pd
    df = pd.read_csv(csv)
    data_list = df.to_dict(orient='records')
    if len(data_list) > category_size:
        data_list = data_list[:category_size]

    checkpoint_file = "checkpoint.json"
    completed_queries = set()
    category_list = []
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            checkpoint_data = json.load(f)
            completed_queries = set(checkpoint_data["completed_queries"])
            category_list = checkpoint_data["category_list"]

    for data in tqdm(data_list):
        if data['query'] in completed_queries:
            continue  # skip completed or errored queries

        try:
            query_type = classify(data['query'])
            category_list.append({
                "query": data['query'],
                "query_type": query_type,
            })

            completed_queries.add(data['query'])
            checkpoint_data = {
                "completed_queries": list(completed_queries),
                "category_list": category_list
            }
            with open(checkpoint_file, "w") as f:
                json.dump(checkpoint_data, f)
        except Exception as e:
            print(f"Error: {e}")
            continue

    to_classification_csv(category_list, output)


if __name__ == '__main__':
    cli()
