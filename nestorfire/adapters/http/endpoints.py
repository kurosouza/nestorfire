import uuid
import datetime
from flask import Flask, request, jsonify, Blueprint
from . import config
from nestorfire.domain.messages import AddFireEntry

bp = Blueprint("nestorfire", __name__,)

@bp.route("/fires", methods=["POST"])
def report_fire():
    fid = uuid.uuid4()
    cmd = AddFireEntry(fid=fid, **request.get_json(), created_on = str(datetime.datetime.now()))
    config.bus.handle(cmd)
    return "", 201, {"Location": "/fires/" + str(fid)}


@bp.route("/fires/<fid>")
def get_fire_info(fid):
    view_builder = config.fireentry_view_builder
    view = view_builder.fetch(uuid.UUID(fid))
    return jsonify(view)


@bp.route("/fires", methods=["GET"])
def list_fires():
    view_builder = config.fireentry_list_builder
    view = view_builder.fetch()
    return jsonify(view)