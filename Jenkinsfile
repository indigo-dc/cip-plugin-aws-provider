#!/usr/bin/groovy

@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/1.4.0']) _

pipeline {
    agent {
        label 'python3.6'
    }

    stages {
        stage('Code fetching') {
            steps {
                checkout scm
            }
        }

        stage('Style analysis') {
            steps {
                ToxEnvRun('pep8')
            }
            post {
                always {
                    WarningsReport('Pep8')
                }
            }
        }

		stage('Metrics gathering') {
            agent {
                label 'sloc'
            }
            steps {
                checkout scm
                SLOCRun()
            }
            post {
                success {
                    SLOCPublish()
                }
            }
        }

        stage('Security scanner') {
            steps {
                ToxEnvRun('bandit-report')
                script {
                    if (currentBuild.result == 'FAILURE') {
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    HTMLReport("/tmp/bandit", 'index.html', 'Bandit report')
                }
            }
        }
	}
}
