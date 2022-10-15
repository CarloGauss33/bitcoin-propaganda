import os
from dotenv import load_dotenv

load_dotenv()

class ConfigVariables:
    def __init__(self) -> None:
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.chat_ids_path = os.getenv("CHAT_IDS_PATH")
        self.memes_path = os.getenv("MEMES_PATH")
        self.meme_state_path = os.getenv("MEMES_STATE_PATH")
        self.chat_ids = self._load_chat_ids()
        self.quotes_path = os.getenv('QUOTES_PATH', 'data/satoshi_quotes.json')

    def _load_chat_ids(self) -> list:
        if not os.path.exists(self.chat_ids_path):
            open(self.chat_ids_path, "w").close()
            return []

        with open(self.chat_ids_path, "r") as f:
            return [ line.strip() for line in f ]

    def _store_chat_ids(self) -> None:
        with open(self.chat_ids_path, "w") as f:
            for chat_id in self.chat_ids:
                f.write(f"{chat_id}\n")

    def add_chat_id(self, chat_id: str) -> None:
        if chat_id not in self.chat_ids:
            self.chat_ids.append(chat_id)
            self._store_chat_ids()

    def remove_chat_id(self, chat_id: str) -> None:
        if chat_id in self.chat_ids:
            self.chat_ids.remove(chat_id)
            self._store_chat_ids()

    def chat_id_in_list(self, chat_id: str) -> bool:
        return chat_id in self.chat_ids



config = ConfigVariables()
