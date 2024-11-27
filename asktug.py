from enum import Enum
from typing import List, Tuple, Optional

import httpx
from retry import retry

from model import Topic

# Get the topics of AskTug, https://asktug.com/, and the best answer of each topic.
# The topic logic is as follows:
#   1. Select some categories:
#     - "TiDB 技术问题"(30022)
#     - "应用开发者专区"(30055)
#     - "其他技术问题"(150022)
#   2. Get the most viewed Top 200 topics of each category.
#   3. Download the best Q&A of each topic.


class AskTUGCategories(Enum):
    tidb = 30022
    developer = 30055
    ecosystem = 150022


@retry(tries=3, delay=2)
def get_topics(
        base_url: str = "https://asktug.com",
        categories_ids: Tuple[int] = (
            AskTUGCategories.tidb.value,
            AskTUGCategories.developer.value,
            AskTUGCategories.ecosystem.value
        ),
        max_topics_per_category: int = 100
) -> List[Topic]:
    topics = []
    for category_id in categories_ids:
        topics_without_answer = get_topics_by_category(base_url, category_id, max_topics_per_category)
        print(f"Got topics, ids of topics: {', '.join([str(topic.id) for topic in topics_without_answer])}")

        for topic in topics_without_answer:
            question_posts, accepted_answer = get_question_and_accept_answer(topic)
            topic.question_posts = question_posts
            topic.accepted_answer = accepted_answer
            if topic.accepted_answer:
                topics.append(topic)
                print(f"Got accept answer of topic: {topic.id}")

    return topics


@retry(tries=3, delay=2)
def get_topics_by_category(
        base_url: str,
        category_id: int,
        max_topics: int
) -> List[Topic]:
    # per page 30 topics, leave some buffer
    max_page = max_topics // 20 + 1

    topics = []
    for page_index in range(0, max_page):
        print(f"Start to get topics, category_id: {category_id}, page: {page_index}")

        url = f"{base_url}/c/{category_id}.json?order=views&page={page_index}"
        response = httpx.get(url, follow_redirects=True)
        data = response.json()
        filtered_topics = [Topic(**topic) for topic in data["topic_list"]["topics"] if topic.get("has_accepted_answer")]
        topics.extend(filtered_topics)

        if len(topics) >= max_topics:
            topics = topics[:max_topics]
            break

    return topics


@retry(tries=3, delay=2)
def get_question_and_accept_answer(topic: Topic) -> (List[str], Optional[str]):
    print(f"Start to get accept answer, topic id: {topic.id}")
    if not topic.has_accepted_answer:
        return None, None

    url = f"https://asktug.com/t/{topic.id}.json"
    response = httpx.get(url, follow_redirects=True)
    data = response.json()
    post_stream = data["post_stream"]
    post_stream_posts = post_stream["posts"]
    question_post = []

    for post in post_stream_posts:
        if post["accepted_answer"]:
            return question_post, get_raw_post(post["id"])
        else:
            question_post.append(get_raw_post(post["id"]))

    return None, None


@retry(tries=3, delay=2)
def get_raw_post(post_id: int) -> str:
    r = httpx.get(f"https://asktug.com/posts/{post_id}.json")
    post = r.json()
    return post["raw"]


if __name__ == "__main__":
    test_topics = get_topics(
        max_topics_per_category=1
    )
    print(test_topics)
