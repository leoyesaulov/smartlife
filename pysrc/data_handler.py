from dotenv import load_dotenv, find_dotenv, set_key, get_key

class DataHandler:
    def __init__(self):
        self.dotenv_file = find_dotenv()
        load_dotenv(self.dotenv_file)

    def write(self, key: str, value: str):
        load_dotenv(self.dotenv_file)
        set_key(self.dotenv_file, key.upper(), value)

    def get(self, key: str) -> str | None:
        load_dotenv(self.dotenv_file)
        return get_key(self.dotenv_file, key.upper())