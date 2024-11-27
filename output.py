from typing import List
import csv

from tqdm import tqdm

from classification import classify
from model import Topic


def safe_value(value):
    if value is None:
        return ""
    if isinstance(value, str):
        # Replace newline characters with escape sequences
        return value.replace("\n", "\\n").replace("\r", "\\r")
    return value


def to_jsonl(topics: List[Topic], file_path: str):
    with open(file_path, "w") as f:
        for topic in topics:
            f.write(topic.model_dump_json() + "\n")


def to_autoflow_eval_dataset(topics: List[Topic], file_path: str):
    # Define the headers
    headers = ["id", "query", "reference", "topic_type"]

    # Open the file and write data
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(headers)  # Write the header row

        for topic in tqdm(topics):
            accepted_answer = topic.accepted_answer
            # Write each topic as a row, using safe_value to handle None
            material = "\\n".join([f"Material: {safe_value(post)}" for post in topic.question_posts])
            query = f"Title: {safe_value(topic.title)}\\n\\n Content: {material}"
            writer.writerow([
                safe_value(topic.id),
                safe_value(query),
                safe_value(accepted_answer),
                safe_value(classify(query)),
            ])


def to_classification_csv(type_object_list: List, file_path: str):
    headers = ["query", "query_type"]

    # Open the file and write data
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(headers)  # Write the header row

        for type_object in type_object_list:
            # Write each topic as a row, using safe_value to handle None
            writer.writerow([
                safe_value(type_object["query"]),
                safe_value(type_object["query_type"]),
            ])
