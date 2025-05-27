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
                    sh 'zip -r tgbot.zip .'
                }
            }
        }
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'tgbot.zip', fingerprint: true
            }
        }
    }
}
