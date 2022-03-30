import json
import os

from flask import request, g

class JsonObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)



def initialize_before_calls(app):
    @app.before_request
    def set_page(page=1):
        page = int(request.args.get('page', 1))
        g.page = page




def init_app(
        app,
        is_init_db: bool = True,
        is_init_kafka: bool = False,
        is_re_init_db: bool = False,
        is_create_admin_logins: bool = False
):
    if is_init_db:
        print("db_inited")





