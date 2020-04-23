import uuid
import datetime
from flask import Flask, request, jsonify
from . import config
from nestorfire.domain.messages import AddFireEntry

app = Flask("nestorfire")

@app.route("/fires", methods=["POST"])
def report_fire():
    fid = uuid.uuid4()
    cmd = AddFireEntry(fid=fid, **request.get_json(), created_on = str(datetime.datetime.now()))
    config.bus.handle(cmd)
    return "", 201, {"Location": "/fires/" + str(fid)}


@app.route("/fires/<fid>")
def get_fire_info(fid):
    view_builder = config.fireentry_view_builder
    view = view_builder.fetch(uuid.UUID(fid))
    return jsonify(view)


@app.route("/fires", methods=["GET"])
def list_fires():
    view_builder = config.fireentry_list_builder
    view = view_builder.fetch()
    return jsonify(view)