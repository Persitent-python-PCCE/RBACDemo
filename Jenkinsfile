pipeline {
    agent any

    triggers{
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

        stage('SonarCloud Analysis'){
            steps{
                script {
                    def scannerHone = tool 'SonarScanner'
                    withSonarQubeEnv('SonarCloud'){
                        bat "\"${scannerHome}\\bin\\sonar-scanner.bat\""
                    }
                }
            }
        }

        stage('Quality Gate'){
            steps{
                timeout(time: 2, unit: 'MINUTES'){
                    waitForQualityGate abortPipeline: true
                }
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

    post{
        success{
            emailext(
                subject: "SUCCESS ${env.JOB_NAME}  #${env.BUILD_NUMBER}",
                body: """
                    <h2>Jenkins build Successful</h2>
                    <p>
                        <b>URL</b>: ${env.BUILD_URL}
                    </p>
                """,
                to: "arulanandha.guru@revature.com"
            )
        }

        failure{
            emailext(
                subject: "FAILED ${env.JOB_NAME}  #${env.BUILD_NUMBER}",
                body: """
                    <h2>Jenkins build Failed</h2>
                    <p>
                        <b>URL</b>: ${env.BUILD_URL}
                    </p>
                """,
                to: "arulanandha.guru@revature.com"
            )
        }
    }

}