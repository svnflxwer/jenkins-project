pipeline {
    agent any

    environment {
        LD_LIBRARY_PATH = '/var/lib/jenkins/workspace/trial/instantclient_11_2'
        ORACLE_HOME     = '/var/lib/jenkins/workspace/trial/instantclient_11_2'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
    
            post {
                failure {
                    script{ 
                        // Send HTML-formatted email notification only when the build fails
                        emailext (
                            subject: "Build Failed: ${currentBuild.fullDisplayName} (${env.BUILD_NUMBER})",
                            body: """<html>
                                        <body>
                                            <h1 style="color:red"> Log output: </h1>
                                            <p>
                                                <pre>\${BUILD_LOG, maxLines = 999}</pre>
                                            </p>
                                        </body>
                                    </html>""",
                            to: "giovanni.harrius@sat.co.id",
                            replyTo: "giovanni.harrius@sat.co.id",
                            mimeType: 'text/html'
                        )
                    }
                }
            }
        }

        stage('Monitor CRON Jobs') {
            steps {
                script {
                    // Set PATH globally
                    def workspaceBin = "${WORKSPACE}/myenv/bin"
                    env.PATH = "${workspaceBin}:${env.PATH}"
                    
                    // Set environment variables
                    sh 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}'
                    sh 'export ORACLE_HOME=${ORACLE_HOME}'
                    sh 'export PATH=${ORACLE_HOME}:${PATH}'
                    sh 'export TNS_ADMIN=/mnt/d/MAGANG-SINAT/oracle-database-xe-11g/app/oracle/product/11.2.0/server/network/ADMIN'

                    // Tambahkan perintah untuk memberikan izin eksekusi pada skrip Python
                    sh "chmod +x ${WORKSPACE}/monitor_cron_jobs.py"
                    sh "chmod +x ${WORKSPACE}/ora.py"

                    // Aktifkan virtual environment (venv)
                    sh "python3 -m venv ${WORKSPACE}/myenv"
                    sh ". ${WORKSPACE}/myenv/bin/activate"

                    // Install Python dependencies and pip
                    sh "${WORKSPACE}/myenv/bin/pip install --upgrade pip"
                    sh "${WORKSPACE}/myenv/bin/pip install -r ${WORKSPACE}/requirementszzz.txt"

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
                        echo "Get Names (Postgre): ${jobNamePg}"
                    }
                    currentBuild.description = jsonDataPg as String
                    
                    for (def jobNameOra : offlineJobsOra) {
                        echo "Get Names (Oracle): ${jobNameOra}"
                    }
                    currentBuild.description = jsonDataOra as String
                }
            }
    
            post {
                failure {
                    script{ 
                        // Send HTML-formatted email notification only when the build fails
                        emailext (
                            subject: "Build Failed: ${currentBuild.fullDisplayName} (${env.BUILD_NUMBER})",
                            body: """<html>
                                        <body>
                                            <h1 style="color:red"> Log output: </h1>
                                            <p>
                                                <pre>\${BUILD_LOG, maxLines = 999}</pre>
                                            </p>
                                        </body>
                                    </html>""",
                            to: "giovanni.harrius@sat.co.id",
                            replyTo: "giovanni.harrius@sat.co.id",
                            mimeType: 'text/html'
                        )
                    }
                }
            }
        }

        stage('Send Email Notifications') {
            steps {
                script {
                    def scriptOutput = currentBuild.description
                    if (scriptOutput) {
                        def emailBody = "The following CRON jobs are offline:\n\n ${scriptOutput}"
                         {

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
    
            post {
                failure {
                    script{ 
                        // Send HTML-formatted email notification only when the build fails
                        emailext (
                            subject: "Build Failed: ${currentBuild.fullDisplayName} (${env.BUILD_NUMBER})",
                            body: """<html>
                                        <body>
                                            <h1 style="color:red"> Log output: </h1>
                                            <p>
                                                <pre>\${BUILD_LOG, maxLines = 999}</pre>
                                            </p>
                                        </body>
                                    </html>""",
                            to: "giovanni.harrius@sat.co.id",
                            replyTo: "giovanni.harrius@sat.co.id",
                            mimeType: 'text/html'
                        )
                    }
                }
            }
        }
    }
}