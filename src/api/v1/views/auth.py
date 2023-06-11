import http
import json

from flask_restx import Namespace, Resource, reqparse
from flask import request

auth_ns = Namespace('api/v1/auth')


@auth_ns.route('/login')
class LoginView(Resource):
    @staticmethod
    def post():
        user_agent = request.headers.get('User-Agent')
        login_parser = reqparse.RequestParser()
        login_parser.add_argument(
            'login',
            type=str,
            required=True,
            help='The user\'s login'
        )
        login_parser.add_argument(
            'password',
            type=str,
            required=True,
            help='The user\'s password'
        )

        args = login_parser.parse_args()
        login: str = args.get('login')
        password: str = args.get('password')

        authy = auth_service.login(login, password, user_agent)
        if not authy:
            return {"message": "Incorrect username or password"}, http.HTTPStatus.UNAUTHORIZED
        return authy, http.HTTPStatus.OK
