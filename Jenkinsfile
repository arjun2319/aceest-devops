pipeline {
    agent any
    
    stages {
        
        stage('Checkout') {
            steps {
                echo 'Code checked out successfully'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running pytest tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t aceest-app:latest .'
            }
        }
        
    }
    
    post {
        success {
            echo 'Pipeline PASSED!'
        }
        failure {
            echo 'Pipeline FAILED!'
        }
    }
}