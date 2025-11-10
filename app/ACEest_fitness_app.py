from flask import Flask, jsonify, request, abort
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['APP_VERSION'] = os.environ.get('APP_VERSION', 'v1.0')

    # simple in-memory data to mimic gym members and classes
    app.members = []
    app.classes = [
        { "id": 1, "name": "Morning Yoga", "duration_min": 45 },
        { "id": 2, "name": "HIIT Blast", "duration_min": 30 },
        { "id": 3, "name": "Strength Training", "duration_min": 60 }
    ]

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify(status='UP', timestamp=datetime.utcnow().isoformat()), 200

    @app.route('/version', methods=['GET'])
    def version():
        return jsonify(version=app.config['APP_VERSION']), 200

    @app.route('/', methods=['GET'])
    def index():
        return jsonify(message='Welcome to ACEest Fitness API', version=app.config['APP_VERSION']), 200

    @app.route('/api/classes', methods=['GET'])
    def list_classes():
        return jsonify(classes=app.classes), 200

    @app.route('/api/members', methods=['GET'])
    def list_members():
        return jsonify(members=app.members), 200

    @app.route('/api/members', methods=['POST'])
    def add_member():
        payload = request.get_json() or {}
        name = payload.get('name')
        age = payload.get('age')
        if not name or not isinstance(age, int):
            abort(400, description='Invalid payload. Provide name (string) and age (integer).')
        member = { 'id': len(app.members)+1, 'name': name, 'age': age, 'joined_at': datetime.utcnow().isoformat() }
        app.members.append(member)
        return jsonify(member=member), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
