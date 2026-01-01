pipeline {
    agent any

    environment {
        IMAGE_NAME = "azizbamar/plant_recognition_model"
        IMAGE_TAG  = "latest"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                  set -e
                  export DOCKER_BUILDKIT=0
                  docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'azizbamar-dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh '''
                  docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to k3s') {
            steps {
                sh '''
                  export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
                  kubectl apply -f /opt/k8s
                  kubectl rollout restart deployment/plant-recognition
                  kubectl rollout status deployment/plant-recognition
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD completed successfully"
        }
        failure {
            echo "❌ CI/CD failed"
        }
    }
}
