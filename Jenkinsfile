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
                    python3 -m venv venv
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
                    python3 -m pytest tests/ -v
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
            echo '✅ Pipeline PASSED! All stages completed successfully.'
        }
        failure {
            echo '❌ Pipeline FAILED! Check the logs above.'
        }
    }
}