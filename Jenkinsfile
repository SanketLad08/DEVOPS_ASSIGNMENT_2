pipeline {
  agent any
  environment {
    IMAGE = "aceest_fitness_local"
    TAG = "${env.BUILD_ID}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Workspace Debug') {
      steps {
        echo "===== Workspace listing ====="
        sh 'pwd; ls -la; echo "---- root files ----"; ls -la . || true; echo "---- app dir ----"; ls -la app || true; echo "---- show file app/requirements.txt ----"; if [ -f app/requirements.txt ]; then echo "requirements exists:"; sed -n "1,200p" app/requirements.txt; else echo "app/requirements.txt NOT FOUND"; fi'
      }
    }

    stage('Unit Test (debug)') {
      steps {
        echo "Running Pytest unit tests inside a Python container..."
        sh '''
          mkdir -p reports
          # Debug: show current dir inside container before trying to install
          docker run --rm -v "$PWD":/src -w /src python:3.11-slim bash -lc "echo 'Inside container: '; pwd; ls -la; echo 'Checking app/requirements.txt:'; if [ -f app/requirements.txt ]; then echo 'FOUND'; sed -n '1,200p' app/requirements.txt; else echo 'NOT FOUND'; fi"
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
      when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
      steps {
        echo "Building Docker image..."
        sh "docker build -t ${IMAGE}:${TAG} app/"
      }
    }
  }

  post {
    always { echo "Pipeline finished" }
  }
}
