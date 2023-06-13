import json
from src.config import AppConfig

def read_prompt(prompt_path: str):
    with open(prompt_path, 'r') as prompt:
        raw_prompt = prompt.read()
        return json.loads(raw_prompt)


print(read_prompt(AppConfig().PROMPT_PATH + 'a'))