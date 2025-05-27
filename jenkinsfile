pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build ZIP') {
            steps {
                script {
                    // Создаем архив zip из содержимого репозитория
                    sh 'zip -r output.zip .'
                }
            }
        }
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'output.zip', fingerprint: true
            }
        }
    }
}
