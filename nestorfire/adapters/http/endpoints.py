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
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    view_builder = config.fireentry_list_builder
    view = view_builder.fetch(limit, offset)
    
    return jsonify(view)

@bp.route("/find_fires", methods=["GET"])
def list_fires_for():
    r_data = request.get_json();
    start_date = r_data.get("start")
    end_date = r_data.get("end")
    country = r_data.get("country")

    print("start = {}, end_date = {}, country = {}".format(start_date, end_date, country))
    view_builder = config.fireentry_query_builder
    view = view_builder.fetch(start_date, end_date, country)

    return jsonify(view)