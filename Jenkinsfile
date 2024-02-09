pipeline {
    agent any

    // environment {
    //     // Set environment variables
    //     LD_LIBRARY_PATH = '/home/sinatriaba/instantclient_11_2'
    //     PATH = "/home/sinatriaba/instantclient_11_2:${PATH}"
    //     TNS_ADMIN = '/mnt/d/MAGANG-SINAT/oracle-database-xe-11g/app/oracle/product/11.2.0/server/network/ADMIN'
   
    //     // Append values to existing PATH
    //     // PATH = "${PATH}:${PATH_EXTRA}"
    // }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Monitor CRON Jobs') {
            steps {
                script {
                    // Set PATH globally
                    def workspaceBin = "${WORKSPACE}/myenv/bin"
                    env.PATH = "${workspaceBin}:${env.PATH}"
                    
                    // Set environment variables
                    //sh 'export LD_LIBRARY_PATH=/home/sinatriaba/instantclient_11_2:$LD_LIBRARY_PATH'
                    sh 'export LD_LIBRARY_PATH=/var/lib/jenkins/workspace/trial/instantclient_11_2'
                    sh 'export ORACLE_HOME=/var/lib/jenkins/workspace/trial/instantclient_11_2'
                    sh 'export PATH=$PATH:/var/lib/jenkins/workspace/trial/instantclient_11_2'
                    //sh 'export TNS_ADMIN=/mnt/d/MAGANG-SINAT/oracle-database-xe-11g/app/oracle/product/11.2.0/server/network/ADMIN'
                    sh 'export TNS_ADMIN=/var/lib/jenkins/workspace/trial/instantclient_11_2'

                    // Tambahkan perintah untuk memberikan izin eksekusi pada skrip Python
                    sh "chmod +x ${WORKSPACE}/monitor_cron_jobs.py"
                    sh "chmod +x ${WORKSPACE}/ora.py"
                    // sh "chmod +rx /home/sinatriaba/instantclient_11_2/libclntsh.so"
                    // sh "chmod +r /home/sinatriaba/instantclient_11_2"

                    // Aktifkan virtual environment (venv)
                    sh "python3 -m venv ${WORKSPACE}/myenv"
                    sh ". ${WORKSPACE}/myenv/bin/activate"

                    // Install Python dependencies and pip
                    sh "${WORKSPACE}/myenv/bin/pip install --upgrade pip"
                    sh "${WORKSPACE}/myenv/bin/pip install -r ${WORKSPACE}/requirements.txt"

                    // Jalankan skrip Python
                    def scriptPathPg = "${WORKSPACE}/monitor_cron_jobs.py"
                    def scriptOutputPg = sh(script: "${WORKSPACE}/myenv/bin/python ${scriptPathPg}", returnStdout: true).trim()
                    echo "Python Script Postgre SQL Output:\n${scriptOutputPg}"

                    def scriptPathOra = "${WORKSPACE}/ora.py"
                    def scriptOutputOra = sh(script: "${WORKSPACE}/myenv/bin/python ${scriptPathOra}", returnStdout: true).trim()
                    echo "Python Script Oracle Output:\n${scriptOutputOra}"


                    // Extract the JSON portion from the script output
                    // Postgre
                    def startIndexPg = scriptOutputPg.indexOf('[')
                    def endIndexPg = scriptOutputPg.lastIndexOf(']')
                    def jsonOutputPg = scriptOutputPg.substring(startIndexPg, endIndexPg + 1)
                    // Extract the JSON portion from the script output

                    // Oracle
                    def startIndexOra = scriptOutputOra.indexOf('[')
                    def endIndexOra = scriptOutputOra.lastIndexOf(']')
                    def jsonOutputOra = scriptOutputOra.substring(startIndexOra, endIndexOra + 1)

                    // Parse the JSON output from the Python script
                    def jsonDataPg = readJSON text: jsonOutputPg
                    def offlineJobsPg = jsonDataPg as List<String>

                    def jsonDataOra = readJSON text: jsonOutputOra
                    def offlineJobsOra = jsonDataOra as List<String>
                    
                    // Iterate over offline jobs
                    for (def jobNamePg : offlineJobsPg) {
                        echo "Offline Job (Postgre): ${jobNamePg}"
                    }
                    currentBuild.description = jsonDataPg as String
                    
                    for (def jobNameOra : offlineJobsOra) {
                        echo "Offline Job (Postgre): ${jobNameOra}"
                    }
                    currentBuild.description = jsonDataOra as String
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