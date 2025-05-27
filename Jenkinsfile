pipeline {
    agent any
    stages {
        stage('Zip files') {
            script {
                  zip zipFile: 'tgbot.zip', dir: '.', excludes: 'venv/**'
            }
        }
    }
}
