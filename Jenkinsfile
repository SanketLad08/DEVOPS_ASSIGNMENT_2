pipeline {
  agent any
  environment {
    IMAGE = "aceest_fitness_local"
    TAG   = "${env.BUILD_ID}"
    HOST_WORKDIR = "/home/slad/Desktop/DEVOPS"
    // GHCR username (change if different)
    GHCR_USER = "SanketLad08"
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
        echo "Running pytest in a host-mounted python container (PYTHONPATH=/src)..."
        sh '''
          mkdir -p reports
          docker run --rm -e PYTHONPATH=/src -v /home/slad/Desktop/DEVOPS:/src -w /src python:3.11-slim bash -lc "
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
      when { expression { currentBuild.result != 'FAILURE' } }
      steps {
        echo "Building Docker image from host path ${HOST_WORKDIR}/app ..."
        sh "docker build -t ${IMAGE}:${TAG} ${HOST_WORKDIR}/app"
      }
    }

    stage('Push to GHCR') {
      when { expression { currentBuild.result != 'FAILURE' } }
      steps {
        echo "Pushing image to GHCR..."
        withCredentials([string(credentialsId: 'GHCR_PAT', variable: 'GHCR_TOKEN')]) {
          sh """
            echo "$GHCR_TOKEN" | docker login ghcr.io -u ${GHCR_USER} --password-stdin
            docker tag ${IMAGE}:${TAG} ghcr.io/${GHCR_USER}/aceest_fitness:${TAG}
            docker push ghcr.io/${GHCR_USER}/aceest_fitness:${TAG}
            docker tag ${IMAGE}:${TAG} ghcr.io/${GHCR_USER}/aceest_fitness:latest
            docker push ghcr.io/${GHCR_USER}/aceest_fitness:latest || true
            docker images | grep aceest_fitness || true
          """
        }
      }
    }

    stage('List Built Images') {
      steps {
        sh "docker images | grep aceest_fitness || true"
      }
    }
  }

  post {
    always { echo 'Pipeline finished' }
    success { echo "Build succeeded: image ${IMAGE}:${TAG}" }
    unstable { echo "Build unstable — tests had warnings or non-fatal issues." }
    failure { echo "Build failed — check console output." }
  }
}
