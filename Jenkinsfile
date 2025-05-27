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
                    sh 'tar -czvf tgbot.tar.gz .'  // Создает сжатый gzip архив из текущей директории
                }
            }
        }
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'tgbot.tar.gz', fingerprint: true
            }
        }
    }
}
