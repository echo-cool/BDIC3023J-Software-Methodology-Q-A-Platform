pipeline {
    agent {
        docker {
            image 'python:3.9-buster'
        }
    }
    stages {
        stage('Pre-Tesks') { 
            steps {
                sh 'python -V'
                sh 'pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple'
            }
        }
        stage('Build') { 
            steps {
                sh 'echo "TEST"'
                sh 'python -V'
                sh 'ls'
            }
        }
        stage('Test') { 
            steps {
                sh 'coverage run ModelsTest.py'
                sh 'coverage report -m' 
            }
        }
        stage('Post-Tasks') { 
            steps {
                sh 'echo Done!' 
            }
        }
    }
}