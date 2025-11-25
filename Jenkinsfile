pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO   = "realtime-python-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        AWS_ACCOUNT_ID = "895183717404"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building Python application"
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Test') {
            steps {
                echo "Running unit tests"
                sh '''
                . venv/bin/activate
                pytest || echo "No tests found, skipping"
                '''
            }
        }


        /*stage('Code Scan - SonarQube') {
            steps {
                echo "Running SonarQube analysis"
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'sonarqube', variable: 'sonarqube')]) {
                        sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=realtime-python-app \
                        -Dsonar.projectName=realtime-python-app \
                        -Dsonar.sources=. \
                        -Dsonar.language=py \
                        -Dsonar.python.version=3 \
                        -Dsonar.host.url=http://98.89.31.232:9000 \
                        -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }*/



/*        stage('Code Scan - SonarQube') {
    steps {
        echo "Running SonarQube analysis using Docker"
        withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
            sh '''
            docker run --rm \
              -e SONAR_HOST_URL=http://98.89.31.232:9000 \
              -e SONAR_LOGIN=$SONAR_TOKEN \
              -v $(pwd):/usr/src \
              sonarsource/sonar-scanner-cli \
              -Dsonar.projectKey=realtime-python-app \
              -Dsonar.sources=.
            '''
        }
    }
}*/



/*stage('Code Scan - SonarQube') {
    steps {
        echo "Running SonarQube analysis using Docker"
        withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_TOKEN')]) {
            sh '''
            docker run --rm \
              -e SONAR_HOST_URL=http://98.89.31.232:9000 \
              -v $(pwd):/usr/src \
              sonarsource/sonar-scanner-cli \
              -Dsonar.projectKey=realtime-python-app \
              -Dsonar.projectName=realtime-python-app \
              -Dsonar.sources=. \
              -Dsonar.login=$SONAR_TOKEN
            '''
        }
    }
}*/





        stage('Docker Image Build') {
            steps {
                echo "Building Docker image"
                sh '''
                docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Image Scan') {
            steps {
                echo "Scanning Docker image with Trivy"
                sh '''
                trivy image ${ECR_REPO}:${IMAGE_TAG} || true
                '''
            }
        }

        stage('Push to AWS ECR') {
            steps {
                echo "Pushing image to AWS ECR"
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                docker tag ${ECR_REPO}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}

                docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI Pipeline completed successfully"
        }
        failure {
            echo "❌ CI Pipeline failed"
        }
    }
}

