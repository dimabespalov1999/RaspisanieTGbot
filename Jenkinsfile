pipeline {
    agent any
    stages {
        stage('Zip files') {
            steps {
                  zip zipFile: 'tgbot.zip', dir: '.', excludes: 'venv/**'
            }
        }
    }
}
