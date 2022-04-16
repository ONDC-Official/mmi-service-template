from flask_restplus import Namespace, Resource, reqparse

from main.service.mmi import fetch_tokens, get_auto_complete_by_query, get_place_info_for_eloc, get_place_info_for_latlong


mmi_namespace = Namespace('mmi', description='mmi utils')

@mmi_namespace.route("/fetch_tokens_for_mmi")
class FetchTokens(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        return parser.parse_args()

    def post(self):
        args = self.create_parser_with_args()
        return fetch_tokens()


@mmi_namespace.route("/mmi_query")
class GetPlacesInfoForQuery(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument("query", required=True)
        return parser.parse_args()

    def get(self):
        args = self.create_parser_with_args()
        return get_auto_complete_by_query(**args)


@mmi_namespace.route("/mmi_place_info")
class GetPlacesInfoForEloc(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument("eloc", required=True)
        return parser.parse_args()

    def get(self):
        args = self.create_parser_with_args()
        return get_place_info_for_eloc(**args)

@mmi_namespace.route("/mmi_latlong_info")
class GetPlacesInfoForEloc(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument("lat", required=True)
        parser.add_argument("long", required=True)
        return parser.parse_args()

    def get(self):
        args = self.create_parser_with_args()
        return get_place_info_for_latlong(**args)

