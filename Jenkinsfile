pipeline {
    agent any

    stages {
        stage('Print env variable') {
            steps {
                echo sh(returnStdout: true, script: 'env')
                echo "ENV Var is ${env}"
            }
        }
    }
}