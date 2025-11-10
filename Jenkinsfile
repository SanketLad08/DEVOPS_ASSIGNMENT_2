pipeline {
  agent any
  environment {
    IMAGE = "aceest_fitness_local"
    TAG = "${env.BUILD_ID}"
    HOST_WORKDIR = "/home/slad/Desktop/DEVOPS"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Prepare Host-Mounted Workspace') {
      steps {
        echo "Copying workspace to host-mounted absolute directory (${HOST_WORKDIR})..."
        sh '''
          mkdir -p ${HOST_WORKDIR}
          rm -rf ${HOST_WORKDIR}/*
          cp -a "$WORKSPACE/." ${HOST_WORKDIR}/
          echo "Files copied to ${HOST_WORKDIR}:"
          ls -la ${HOST_WORKDIR} | sed -n '1,300p'
        '''
      }
    }

    stage('Unit Test') {
      steps {
        echo "Running pytest in a host-mounted python container using ${HOST_WORKDIR}..."
        sh '''
          mkdir -p reports
          docker run --rm -v /home/slad/Desktop/DEVOPS:/src -w /src python:3.11-slim bash -lc "
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
        sh "docker build -t ${IMAGE}:${TAG} /home/slad/Desktop/DEVOPS/app"
      }
    }

    stage('List Built Images') {
      steps {
        sh "docker images | grep ${IMAGE} || true"
      }
    }
  }

  post { always { echo 'Pipeline finished' } }
}
