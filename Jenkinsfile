pipeline {
    agent any

    stages {
        stage('Check environment variable') {
            // Checks the environment variable 'RemoteTrigger'.
            steps {
                echo sh(returnStdout: true, script: 'env')
                echo "ENV Var is ${env.RemoteTrigger}"
                sh("This is shell: ${env.RemoteTrigger}")
            }
        }
    }
}