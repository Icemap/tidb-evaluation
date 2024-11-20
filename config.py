from dotenv import load_dotenv
import os


class __Config:
    def __init__(self):
        load_dotenv()

        self.debug = bool(os.getenv("DEBUG", "True") == "True")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_path = os.getenv("LOG_PATH", "./tidb-evaluation.log")
        self.sleep_time = int(os.getenv("SLEEP_TIME", "30"))

        # self.open_ai_base_url = os.getenv("OPEN_AI_BASE_URL", "https://api.openai.com/v1")
        # self.open_ai_api = os.getenv("OPEN_AI_API", "")

        self.en_discourse_host = os.getenv("EN_DISCOURSE_HOST", "")
        self.en_discourse_api_username = os.getenv("EN_DISCOURSE_API_USERNAME", "")
        self.en_discourse_api_key = os.getenv("EN_DISCOURSE_API_KEY", "")
        self.en_discourse_category_id = int(os.getenv("EN_DISCOURSE_CATEGORY_ID"))


conf = __Config()
