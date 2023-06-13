import json

from flask_restx import Namespace, Resource
from flask import request
from flask.app import BadRequest

from src.container import token_generator, open_ai_client,

gpt_ns = Namespace('api/v1/gpt')


@gpt_ns.route('/')
class GPTRequestView(Resource):
    def get(self):
        token = request.headers['access_token']
        token_data = token_generator.check_jwt_token(token)['data']
        username = token_data.get('username')

        req_data = json.loads(request.json)
        topic, student_question = req_data.get('topic'), req_data.get('question')

        if not any([username, topic, student_question]):
            raise BadRequest('Either username, topic or question were not passed')  # TODO add logging

        model_response = open_ai_client.send_api_request(student_question)



