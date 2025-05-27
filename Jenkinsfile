pipeline {
    agent any
    stages {
        stage('Zip files') {
            step {
                  zip zipFile: 'tgbot.zip', dir: '.', excludes: 'venv/**'
            }
        }
    }
}
