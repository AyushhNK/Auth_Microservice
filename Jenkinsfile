pipeline {
    agent any

    environment {
        PROJECT_NAME = "auth_service"
        DOCKER_IMAGE = "auth-service"
        DOCKER_TAG   = "${BUILD_NUMBER}"
        PYTHONUNBUFFERED = "1"
    }

    stages {

        stage("Checkout Code") {
            steps {
                checkout scm
            }
        }

        stage("Build Docker Image") {
            steps {
                script {
                    sh """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    """
                }
            }
        }

        stage("Run Lint & Tests") {
            steps {
                script {
                    sh """
                    docker run --rm \
                        -e DJANGO_SETTINGS_MODULE=core.settings \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        sh -c "
                        python manage.py check &&
                        python manage.py test
                        "
                    """
                }
            }
        }

        stage("Generate gRPC Code") {
            steps {
                script {
                    sh """
                    docker run --rm \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        python -m grpc_tools.protoc \
                          -I proto \
                          --python_out=. \
                          --grpc_python_out=. \
                          proto/auth.proto
                    """
                }
            }
        }

        stage("Security Checks (Optional)") {
            steps {
                script {
                    sh """
                    docker run --rm \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        sh -c "pip install bandit && bandit -r ."
                    """
                }
            }
        }

        stage("Push Docker Image") {
            when {
                branch "main"
            }
            steps {
                script {
                    sh """
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} your_dockerhub/${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push your_dockerhub/${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage("Deploy (Optional)") {
            when {
                branch "main"
            }
            steps {
                echo "Deploy stage (K8s / Docker Swarm / EC2 / VPS)"
                // Example:
                // sh "ssh user@server docker pull your_dockerhub/auth-service:${DOCKER_TAG}"
            }
        }
    }

    post {
        success {
            echo "✅ Auth Service CI Pipeline Passed"
        }
        failure {
            echo "❌ Pipeline Failed"
        }
        always {
            sh "docker system prune -f"
        }
    }
}
