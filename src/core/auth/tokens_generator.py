import base64
import calendar
import datetime
import hashlib
import hmac

import jwt

SALT = b'blablabla'
HASH_NAME = 'sha256'
NUM_ITERS_HASH = 100_000
secret = '$3cr3t'
algo = 'HS256'


class PasswordHasher:
    def __init__(self):
        self.hash_name = HASH_NAME
        self.num_hash_iterations = NUM_ITERS_HASH
        self.salt = SALT

    def hash_password(self, password: str):
        hashed_digest = hashlib.pbkdf2_hmac(
            self.hash_name,
            password.encode('utf-8'),
            self.salt,
            self.num_hash_iterations
        )
        return base64.b64encode(hashed_digest)

    def compare_passwords(self, given_password: str, password_hash: str) -> bool:
        given_password_digest = hashlib.pbkdf2_hmac(
            self.hash_name,
            given_password.encode('utf-8'),
            self.salt,
            self.num_hash_iterations
        )
        password_hash_digest = base64.b64decode(password_hash)
        return hmac.compare_digest(given_password_digest, password_hash_digest)


class TokenGenerator:
    def __init__(self, jwt_config):
        self.jwt_config = jwt_config.dict()
        self.access_expiry_time = self.jwt_config['access_token_lifetime']
        self.refresh_expiry_time = self.jwt_config['refresh_token_lifetime']

    def generate_refresh_and_access_tokens(self, data: dict):
        access_token = self._generate_jwt_token(data, self.access_expiry_time)
        refresh_token = self._generate_jwt_token(data, self.refresh_expiry_time)
        return access_token, refresh_token

    @staticmethod
    def _generate_jwt_token(data: dict, expiry_time_minutes: int) -> str:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_time_minutes)
        data['exp'] = calendar.timegm(expiration.timetuple())
        return jwt.encode(data, secret, algorithm=algo)

    @staticmethod
    def check_jwt_token(token: str) -> dict:
        try:
            token_data = jwt.decode(
                token,
                secret,
                algorithms=[algo]
            )
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return {'result': False, 'msg': 'Token not valid'}
        else:
            return {'result': True, 'msg': 'Token valid', 'data': token_data}


