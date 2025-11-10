pipeline {
  agent any
  environment {
    DOCKER_IMAGE = "your_dockerhub_username/aceest_fitness"
    IMAGE_TAG = "${env.BUILD_ID}"
    REGISTRY = "docker.io"
    KUBE_CONTEXT = "minikube"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps {
        sh 'docker --version || true'
        sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} app'
      }
    }
    stage('Unit Test') {
      steps {
        sh 'pytest -q'
      }
    }
    stage('SonarQube Scan') {
      steps {
        echo 'Run SonarQube scan here (configure Jenkins Sonar plugin)'
      }
    }
    stage('Push Image') {
      steps {
        echo 'Login and push to Docker registry - edit scripts/build_and_push.sh with your creds'
        sh 'bash scripts/build_and_push.sh ${DOCKER_IMAGE} ${IMAGE_TAG}'
      }
    }
    stage('Deploy to K8s') {
      steps {
        echo 'kubectl apply manifests - adjust as needed'
        sh 'kubectl --context=${KUBE_CONTEXT} apply -f k8s/'
      }
    }
  }
  post {
    always {
      echo 'Pipeline finished.'
    }
  }
}
