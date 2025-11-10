from flask import Blueprint, jsonify

schedules_bp = Blueprint("schedules", __name__)

@schedules_bp.route("/api/schedules", methods=["GET"])
def get_schedules():
    return jsonify(schedules=[{"id":1,"class":"Morning Yoga","time":"06:00"},{"id":2,"class":"HIIT Blast","time":"18:00"}])
