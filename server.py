import flask
from flask import request, jsonify, session
from flask.views import MethodView
from db import Session, Advert
from errors import HttpError
from schema import validate, CreateAdvert, UpdateAdvert

app = flask.Flask("app")

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({"error": error.message})
    http_response.status_code = error.status_code
    return http_response

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response

def get_advert_by_id(advert_id: int):
    advert = request.session.get(Advert, advert_id)

    if advert is None:
        raise HttpError(404, "Not found")
    return advert

def add_advert(advert: Advert):
    request.session.add(advert)
    request.session.commit()
    return advert

class AdvertView(MethodView):
    def get(self, advert_id):
        advert = get_advert_by_id(advert_id)
        return jsonify(advert.dict)

    def post(self):
        json_data = validate(CreateAdvert, request.json)

        advert = Advert(title=json_data["title"],
                        description=json_data["description"],
                        owner=json_data["owner"]
                        )
        add_advert(advert)
        return jsonify(advert.dict)

    def patch(self, advert_id):
        json_data = validate(UpdateAdvert, request.json)


        advert = get_advert_by_id(advert_id)
        if "title" in json_data:
            advert.title = json_data["title"]
        if "description" in json_data:
            advert.description = json_data["description"]
        if "owner" in json_data:
            advert.owner = json_data["owner"]

        request.session.commit()
        return jsonify(advert.dict)


    def delete(self, advert_id):
        advert = get_advert_by_id(advert_id)
        request.session.delete(advert)
        request.session.commit()
        return jsonify({"status": "deleted"})


def hello_world(some_id: int):
    json_data = request.json
    headers = request.headers
    qs = request.args

    print(f"{some_id=}")
    print(f"{json_data=}")
    print(f"{headers=}")
    print(f"{qs=}")

    http_response = flask.jsonify({"hello": "world"})
    http_response.status_code = 201
    return http_response

advert_view = AdvertView.as_view("as_view")

app.add_url_rule("/hello/world/<int:some_id>", view_func=hello_world, methods=["POST"])
app.add_url_rule("/advert/", view_func=advert_view, methods=["POST"])
app.add_url_rule("/advert/<int:advert_id>", view_func=advert_view, methods=["GET", "PATCH", "DELETE"])

app.run()