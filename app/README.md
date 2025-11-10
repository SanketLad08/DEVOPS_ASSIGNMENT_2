# ACEest Flask App (app/)

This is a minimal Flask application to represent the ACEest Fitness backend for the assignment.
Endpoints:
- GET /health
- GET /version
- GET /api/classes
- GET /api/members
- POST /api/members  { name: str, age: int }

To run locally:
1. Create virtualenv and install requirements
2. Set APP_VERSION environment variable if you want to override the default
3. Run `python ACEest_fitness_app.py` or use gunicorn (Dockerfile uses gunicorn)
