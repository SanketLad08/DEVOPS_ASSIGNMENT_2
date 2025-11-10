Quick commands (example):

# Build image locally
docker build -t your_dockerhub_username/aceest_fitness:v1.0 app/

# Run container locally
docker run -e APP_VERSION=v1.0 -p 5000:5000 your_dockerhub_username/aceest_fitness:v1.0

# Apply k8s manifests (minikube)
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment-v1.yaml
