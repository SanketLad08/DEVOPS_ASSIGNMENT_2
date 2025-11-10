from flask import Flask, jsonify, request, abort
from datetime import datetime

def create_app():
    app = Flask(__name__)

    # in-memory stores
    app.members = []
    app.classes = [
        {"id": 1, "name": "Morning Yoga", "duration_min": 45},
        {"id": 2, "name": "HIIT Blast", "duration_min": 30},
        {"id": 3, "name": "Strength Training", "duration_min": 60},
    ]
    app.schedules = [
        {"id":1, "class_id":1, "start":"06:30", "day":"Mon"},
        {"id":2, "class_id":2, "start":"18:00", "day":"Tue"},
        {"id":3, "class_id":3, "start":"07:00", "day":"Wed"},
    ]

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify(status='UP', timestamp=datetime.utcnow().isoformat()), 200

    @app.route('/version', methods=['GET'])
    def version():
        return jsonify(version='v1.0')

    @app.route('/api/classes', methods=['GET'])
    def get_classes():
        return jsonify(classes=app.classes)

    @app.route('/api/schedules', methods=['GET'])
    def get_schedules():
        # simple schedule listing
        return jsonify(schedules=app.schedules)

    @app.route('/api/members', methods=['GET'])
    def list_members():
        return jsonify(members=app.members)

    @app.route('/api/members', methods=['POST'])
    def add_member():
        payload = request.get_json() or {}

        # extract values first, then validate
        name = payload.get('name')
        age_raw = payload.get('age')

        # try to coerce age to int if possible
        try:
            age = int(age_raw) if age_raw is not None else None
        except (ValueError, TypeError):
            age = None

        # validation: non-empty name string and positive integer age
        if not isinstance(name, str) or not name.strip() or not isinstance(age, int) or age <= 0:
            return jsonify(error="Invalid payload: 'name' (non-empty string) and 'age' (positive integer) required"), 400

        member = {
            'id': len(app.members) + 1,
            'name': name.strip(),
            'age': age,
            'joined_at': datetime.utcnow().isoformat()
        }
        app.members.append(member)
        return jsonify(member=member), 201

    return app

# convenience for running via 'flask run'
if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5001)
