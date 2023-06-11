from flask_restx import Namespace, Resource


gpt_ns = Namespace('api/v1/gpt')


@gpt_ns.route('/')
class GPTRequestView(Resource):
    def get(self):
        return 'fuck you'