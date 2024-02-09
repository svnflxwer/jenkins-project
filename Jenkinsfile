pipeline {
    agent any

    environment {
        LD_LIBRARY_PATH = '/var/lib/jenkins/instantclient_11_2'
        ORACLE_HOME     = '/var/lib/jenkins/instantclient_11_2'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Create Data Directory') {
            steps {
                // Membuat folder dataCsvTemp jika belum ada
                sh 'mkdir -p /var/lib/jenkins/dataCsvTemp'
            }
        }

        stage('Activate Virtual Environment Python') {
            steps {
                script {
                    // Set PATH globally
                    def workspaceBin = "${WORKSPACE}/myenv/bin"
                    env.PATH = "${workspaceBin}:${env.PATH}"

                    // Aktifkan virtual environment (myenv)
                    sh "python3 -m venv ${WORKSPACE}/myenv"
                    sh ". ${WORKSPACE}/myenv/bin/activate"

                    // Install Python dependencies and pip
                    sh "${WORKSPACE}/myenv/bin/pip install --upgrade pip"
                    sh "${WORKSPACE}/myenv/bin/pip install -r ${WORKSPACE}/requirements.txt"
                }
            }
        }

        stage('Get Data Oracle') {
            steps {
                script {
                    // Set environment variables
                    sh 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}'
                    sh 'export ORACLE_HOME=${ORACLE_HOME}'
                    sh 'export PATH=${ORACLE_HOME}:${PATH}'
                    sh 'export TNS_ADMIN=${ORACLE_HOME}/network/ADMIN'

                    // Tambahkan perintah untuk memberikan izin eksekusi pada skrip Python
                    sh "chmod +x ${WORKSPACE}/selectOra.py"

                    // Jalankan skrip Python

                    def scriptPathOra = "${WORKSPACE}/selectOra.py"
                    def scriptOutputOra = sh(script: "${WORKSPACE}/myenv/bin/python ${scriptPathOra}", returnStdout: true).trim()
                    echo "Python Script Oracle Output:\n${scriptOutputOra}"

                    // Extract the JSON portion from the script output
                    // Oracle
                    def startIndexOra = scriptOutputOra.indexOf('[')
                    def endIndexOra = scriptOutputOra.lastIndexOf(']')
                    def jsonOutputOra = scriptOutputOra.substring(startIndexOra, endIndexOra + 1)

                    // Parse the JSON output from the Python script

                    def jsonDataOra = readJSON text: jsonOutputOra
                    def offlineJobsOra = jsonDataOra as List<String>
                    
                    for (def jobNameOra : offlineJobsOra) {
                        echo "Get Names (Oracle): ${jobNameOra}"
                    }
                    currentBuild.description = jsonDataOra as String
                }
            }
        }

        stage('Get Data Postgre') {
            steps {
                script {
                    // Tambahkan perintah untuk memberikan izin eksekusi pada skrip Python
                    sh "chmod +x ${WORKSPACE}/insertPG.py"

                    // Jalankan skrip Python
                    def scriptPathPg = "${WORKSPACE}/insertPG.py"
                    def scriptOutputPg = sh(script: "${WORKSPACE}/myenv/bin/python ${scriptPathPg}", returnStdout: true).trim()
                    echo "Python Script Postgre SQL Output:\n${scriptOutputPg}"


                    // Extract the JSON portion from the script output
                    // Postgre
                    def startIndexPg = scriptOutputPg.indexOf('[')
                    def endIndexPg = scriptOutputPg.lastIndexOf(']')
                    def jsonOutputPg = scriptOutputPg.substring(startIndexPg, endIndexPg + 1)

                    // Parse the JSON output from the Python script
                    def jsonDataPg = readJSON text: jsonOutputPg
                    def offlineJobsPg = jsonDataPg as List<String>

                    // Iterate over offline jobs
                    for (def jobNamePg : offlineJobsPg) {
                        echo "Get Names (Postgre): ${jobNamePg}"
                    }
                    currentBuild.description = jsonDataPg as String
                }
            }
        }

        stage('Send Email Notifications') {
            steps {
                script {
                    def scriptOutput = currentBuild.description
                    if (scriptOutput) {
                        def emailBody = "The following CRON jobs are offline:\n\n ${scriptOutput}"
                        withCredentials([usernamePassword(credentialsId: 'gmail', usernameVariable: 'SMTP_USERNAME', passwordVariable: 'SMTP_PASSWORD')]) {

                            emailext(
                                subject: "CRON Jobs Status ${env.JOB_NAME} (${env.BUILD_NUMBER}",
                                body: emailBody,
                                to: 'giovanni.harrius@sat.co.id',
                                replyTo: 'giovanni.harrius@sat.co.id'
                            )
                        }
                    }
                }
            }
        }
    }
}