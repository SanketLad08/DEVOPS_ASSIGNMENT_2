pipeline {
  agent any
  environment {
    IMAGE = "aceest_fitness_local"
    TAG = "${env.BUILD_ID}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Unit Test') {
      steps {
        echo "Running Pytest unit tests..."
        sh '''
          mkdir -p reports
          docker run --rm -v "$PWD":/src -w /src python:3.11-slim bash -lc "
            pip install --no-cache-dir -r app/requirements.txt pytest pytest-cov &&
            pytest -q --junitxml=reports/junit.xml --cov=app --cov-report=xml:reports/coverage.xml
          "
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/junit.xml'
          archiveArtifacts artifacts: 'reports/**', fingerprint: true
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        echo "Building Docker image..."
        sh "docker build -t ${IMAGE}:${TAG} app/"
      }
    }

    stage('List Built Images') {
      steps {
        echo "Listing built Docker images..."
        sh "docker images | grep aceest_fitness || true"
      }
    }
  }

  post {
    success {
      echo "✅ CI pipeline finished successfully!"
    }
    failure {
      echo "❌ CI pipeline failed. Check the console output for details."
    }
  }
}
