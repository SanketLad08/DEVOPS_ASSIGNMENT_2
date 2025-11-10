# ACEest Fitness - DevOps CI/CD Project (Prepared)

This archive contains a ready-to-run project for the ACEest Fitness & Gym DevOps CI/CD assignment.
Files included:
- app/ : Flask application, Dockerfile, and requirements
- tests/ : Pytest tests
- k8s/ : Kubernetes manifests (examples for blue-green, canary, rolling update)
- Jenkinsfile : Declarative pipeline example
- sonar-project.properties : SonarQube configuration
- scripts/build_and_push.sh : Example build and push script (edit before use)
- .gitignore

How to use (quick):
1. Copy the zip to your Linux VM and extract:
   ```bash
   unzip ACEest_DevOps_Pipeline.zip -d ACEest_DevOps_Pipeline
   cd ACEest_DevOps_Pipeline/app
   ```
2. Build & run locally for quick test:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   export FLASK_APP=ACEest_fitness_app:create_app
   export APP_VERSION=v1.0
   flask run --host=0.0.0.0 --port=5000
   ```
   Or build Docker image:
   ```bash
   docker build -t <your_dockerhub_username>/aceest_fitness:v1.0 .
   ```
3. Run tests:
   ```bash
   pytest -q
   ```

Notes:
- Edit `scripts/build_and_push.sh`, `Jenkinsfile`, and `sonar-project.properties` to add your credentials and SonarQube/DockerHub values.
- Kubernetes manifests are examples targeted at Minikube / local clusters. Adjust image names, namespaces, and ingress according to your environment.
