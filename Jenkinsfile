pipeline {
    agent any
    stages {
        stage('Zip files') {
            steps {
                zip zipFile: 'tgbot.zip', dir: '.', overwrite: true, archive: true, exclude: 'venv/**'

                 
            }
        }
    }
}
