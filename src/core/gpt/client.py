import abc
import json
import random

import requests

from src.config import ModelEnvironments, AppConfig


def mock_request():
    mock_responses = [
        'First mock response',
        'Second mock response'
    ]
    return random.choice(mock_responses)


class BaseGPTClient(abc.ABC):
    @abc.abstractmethod
    def send_api_request(self, prompt: str, tag: str):
        pass


class OpenAIClient(BaseGPTClient):
    def __init__(self, url: str, token: str = None):
        self.url = url
        self.token = token
        self.sessions: dict[str, requests.Session] | None = {}

    def send_api_request(self, prompt: str, tag: str):
        """
        Sends HTTP requests to language model API
        :param prompt: includes prompt constraint of language model and ingested student question
        :return:
        """
        if AppConfig.MODEL_ENVIRONMENT == ModelEnvironments.dev:
            return mock_request()

        session = self.sessions.get(tag)
        if not session:
            session = requests.session()
            self.sessions[tag] = session

        response = session.get(
            url=self.url, json=json.dumps(prompt)
        )
        return response.json()





