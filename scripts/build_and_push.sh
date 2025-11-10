#!/bin/bash
# Example build and push script.
# Usage: ./scripts/build_and_push.sh <image_name> <tag>
IMAGE_NAME=${1:-your_dockerhub_username/aceest_fitness}
TAG=${2:-latest}

if [ -z "$DOCKER_USERNAME" ] || [ -z "$DOCKER_PASSWORD" ]; then
  echo "Please set DOCKER_USERNAME and DOCKER_PASSWORD env vars or login manually before running this script."
  exit 0
fi

docker build -t ${IMAGE_NAME}:${TAG} app
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push ${IMAGE_NAME}:${TAG}
