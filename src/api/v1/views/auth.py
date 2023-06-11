import http

from flask_restx import Namespace, Resource, reqparse

from src.container import auth_service, user_dao

auth_ns = Namespace('api/v1/auth')


def parse_args() -> tuple[str, str]:
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
    return args.get('login'), args.get('password')


@auth_ns.route('/login')
class LoginView(Resource):
    @staticmethod
    def post():
        login, password = parse_args()

        auth_response = auth_service.login(login, password)
        if not auth_response:
            return {"message": "Incorrect username or password"}, http.HTTPStatus.UNAUTHORIZED
        return auth_response, http.HTTPStatus.OK


@auth_ns.route('/signup')
class SignUpView(Resource):
    def post(self):
        login, password = parse_args()

        if user_dao.get_user(login):
            return {'message': 'User already exists'}, http.HTTPStatus.BAD_REQUEST

        auth_service.signup(login, password)
        return {'message': 'User created successfully'}, http.HTTPStatus.CREATED

