pipeline {
  agent any
  environment {
    IMAGE = "aceest_fitness_local"
    TAG = "${env.BUILD_ID}"
    HOST_WORKDIR = "/workspace/DEVOPS" // host-mounted path inside Jenkins container
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Prepare Host-Mounted Workspace') {
      steps {
        echo "Copying workspace to host-mounted directory so host Docker can access sources..."
        // ensure destination exists and is writable
        sh '''
          mkdir -p ${HOST_WORKDIR}
          # remove old copy to avoid stale files
          rm -rf ${HOST_WORKDIR}/*
          # copy current workspace (this is inside the Jenkins container) to the mounted host path
          cp -a "$WORKSPACE/." ${HOST_WORKDIR}/
          echo "Files copied to ${HOST_WORKDIR}:"
          ls -la ${HOST_WORKDIR} | sed -n '1,200p'
        '''
      }
    }

    stage('Unit Test') {
      steps {
        echo "Running Pytest unit tests inside a Python container (host mounted)..."
        sh '''
          mkdir -p reports
          # Run container mounting the host-mounted copy so host docker sees files
          docker run --rm -v ${HOST_WORKDIR}:/src -w /src python:3.11-slim bash -lc "
            pip install --no-cache-dir -r app/requirements.txt pytest pytest-cov &&
            pytest -q --junitxml=reports/junit.xml --cov=app --cov-report=xml:reports/coverage.xml || true
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
      when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
      steps {
        echo "Building Docker image using host-mounted workspace..."
        sh "docker build -t ${IMAGE}:${TAG} ${HOST_WORKDIR}/app"
      }
    }

    stage('List Built Images') {
      steps {
        sh "docker images | grep ${IMAGE} || true"
      }
    }
  }

  post {
    always { echo "Pipeline finished" }
  }
}
