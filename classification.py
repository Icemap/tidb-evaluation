from enum import Enum

import openai
from pydantic import BaseModel


classify_prompt = """
As an AI assistant, you will act as an agent to classify user queries into the following categories:

1. Basic Knowledge: Queries about simple facts or common knowledge regarding TiDB, such as configuration parameters, component design, etc.
2. Operation Guide: Users seeking instructions on how to perform a specific operation they are unsure about.
3. Problem Troubleshooting: Users encountering error messages or unexpected results and wanting to identify and solve the issue.
4. Complex Task Planning: Users setting a complex goal that requires multiple steps, seeking a comprehensive plan or guidance.
5. Other Topics: Questions unrelated to TiDB or databases, or general discussion topics.

Your task is to carefully read the Title and Content of the user's query and assign it to one of the above categories. 
Provide only the classification level (e.g., "Level-1 Basic Knowledge") and do not include any additional information.
"""


class QueryType(str, Enum):
    BasicKnowledge = "Basic Knowledge"
    OperationGuide = "Operation Guide"
    ProblemTroubleshooting = "Problem Troubleshooting"
    ComplexTaskPlanning = "Complex Task Planning"
    OtherTopics = "Other Topics"


class ClassifyResponse(BaseModel):
    type: QueryType


def classify(query: str) -> QueryType:
    # Classify the query to one of the types
    # See the document: https://platform.openai.com/docs/guides/structured-outputs
    completion = openai.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": classify_prompt},
            {"role": "user", "content": query},
        ],
        response_format=ClassifyResponse,
    )

    event = completion.choices[0].message.parsed
    return event.type
