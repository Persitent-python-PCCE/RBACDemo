pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                bat '''
                    python3 -m pip install -r requirements.txt
                    python3 -m pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build -t arulguru03/flask-app:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat '''
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push arulguru03/flask-app:latest
                    '''
                }
            }
        }
    }
}