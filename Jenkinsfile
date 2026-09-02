pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                bat '''
                    "C:\\Users\\ArulanandhaGuru\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" --version
                    "C:\\Users\\ArulanandhaGuru\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install -r requirements.txt
                    "C:\\Users\\ArulanandhaGuru\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pytest
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

    post {

        success {
            emailext(
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Jenkins Build Successful</h2>

                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> SUCCESS</p>
                    <p><b>Build URL:</b> ${env.BUILD_URL}</p>

                    <p>
                        Tests passed, SonarCloud analysis completed,
                        Docker image was built and pushed successfully.
                    </p>
                """,
                to: "your-email@example.com"
            )
        }

        failure {
            emailext(
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Jenkins Build Failed</h2>

                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> FAILED</p>
                    <p><b>Build URL:</b> ${env.BUILD_URL}</p>

                    <p>
                        One or more pipeline stages failed.
                        Please check the Jenkins console output.
                    </p>
                """,
                to: "your-email@example.com"
            )
        }
    }
}