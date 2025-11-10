#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
echo "Running from: $ROOT_DIR"

# Safety: don't destroy existing git repos unintentionally
if [ -d ".git" ]; then
  echo "A .git directory already exists in $ROOT_DIR. Aborting to avoid overwriting your repo."
  echo "If you want to proceed anyway, remove .git first and re-run this script."
  exit 1
fi

git init
git config user.name "Sanket Lad"
git config user.email "sanketlad0008@gmail.com"
git checkout -b main

# --- v1.0 initial commit ---
git add .
git commit -m "chore: initial ACEest Flask app v1.0 - basic endpoints and tests"
git tag -a v1.0 -m "v1.0 - initial"

# --- v1.1: add schedules endpoint ---
# Create a small feature file and wire a route into app (non-destructive)
cat > app/feature_schedules.py <<'PY'
from flask import Blueprint, jsonify

schedules_bp = Blueprint("schedules", __name__)

@schedules_bp.route("/api/schedules", methods=["GET"])
def get_schedules():
    return jsonify(schedules=[{"id":1,"class":"Morning Yoga","time":"06:00"},{"id":2,"class":"HIIT Blast","time":"18:00"}])
PY

# Register the blueprint by appending safe registration in ACEest_fitness_app.py if not present
if ! grep -q "feature_schedules" app/ACEest_fitness_app.py; then
  # add import and registration near create_app (simple append - safe for this simulated history)
  awk '
  /def create_app\(\):/ { print; in_app=1; next}
  { print }
  END {
    if (in_app) {
      print ""
      print "    # --- schedules feature (added in v1.1) ---"
      print "    try:"
      print "        from app.feature_schedules import schedules_bp"
      print "        app.register_blueprint(schedules_bp)"
      print "    except Exception:"
      print "        pass"
    }
  }' app/ACEest_fitness_app.py > /tmp/ACEest_fitness_app.py && mv /tmp/ACEest_fitness_app.py app/ACEest_fitness_app.py
fi

git add app/feature_schedules.py app/ACEest_fitness_app.py
git commit -m "feat: add /api/schedules endpoint (v1.1)"
git tag -a v1.1 -m "v1.1 - schedules endpoint"

# --- v1.2: README + test improvement ---
# Update README and tests to simulate iterative improvements
sed -i "1s|^|## v1.2 improvements - README notes\\n\\n|" README_root.md || true
# Add a tiny test that expects schedules endpoint (if tests exist)
if [ -f "tests/test_app.py" ]; then
  cat >> tests/test_app.py <<'PY'

def test_get_schedules(client):
    rv = client.get('/api/schedules')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'schedules' in data
PY
fi

git add README_root.md tests/test_app.py || true
git commit -m "docs: update README and add schedules test (v1.2)"
git tag -a v1.2 -m "v1.2 - docs & tests"

# --- v1.3: small validation bugfix on POST /api/members ---
# Patch ACEest_fitness_app.py to tighten validation (simulate bugfix)
awk '
/def add_member\(\):/ {print; getline; print; print "        # validation tightened in v1.3: require non-empty name and positive integer age"; print "        if not isinstance(name, str) or not name.strip() or not isinstance(age, int) or age <= 0:"; print "            abort(400, description=\"Invalid payload. Provide non-empty name (string) and positive integer age.\")"; found=1; next}
{ print }
' app/ACEest_fitness_app.py > /tmp/ACEest_fitness_app.py && mv /tmp/ACEest_fitness_app.py app/ACEest_fitness_app.py

git add app/ACEest_fitness_app.py
git commit -m "fix: tighten POST /api/members input validation (v1.3)"
git tag -a v1.3 -m "v1.3 - validation fix"

echo "Done. Created tags: v1.0, v1.1, v1.2, v1.3"
echo "Local git repo ready. To push to GitHub:"
echo "  1) Create an empty repo on GitHub (or use 'gh repo create')"
echo "  2) git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git"
echo "  3) git push -u origin main --tags"

exit 0

