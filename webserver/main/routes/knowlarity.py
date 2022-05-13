from flask_restplus import Namespace, Resource, reqparse

from main.service.knowlarity import call_patron

knowlarity_namespace = Namespace('knowlarity', description='knowlarity namespace')

@knowlarity_namespace.route("/call-patron")
class FetchTokens(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_phone_number",required=True)
        parser.add_argument("seller_phone_number",required=True)
        return parser.parse_args()

    def post(self):
        args = self.create_parser_with_args()
        return call_patron(**args)
