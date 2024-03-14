pipeline {
    agent any

    environment {
        LD_LIBRARY_PATH = '/home/giovannih/oracle/instantclient_11_2'
        ORACLE_HOME     = '/home/giovannih/oracle/instantclient_11_2'
        CSV_FILE_PATH   = '/var/lib/jenkins/dataCsvTemp'
        SQL_FILE_PATH   = '/var/lib/jenkins/workspace/finance-dept_transaksi-penjualan-retail_pg-to-ora'
        PG_HOST         = 'localhost'
        PG_PORT         = '5432'
        PG_DATABASE     = 'postgres'
        PG_USER         = 'postgres'
        PG_PASSWORD     = 'iamhuman'
        ORACLE_USER     = 'giovanni'
        ORACLE_PASSWORD = 'iamhuman'
        ORACLE_HOST     = 'localhost'
        ORACLE_PORT     = '1521'
        ORACLE_SID      = 'XE'
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
                        withCredentials([usernamePassword(credentialsId: 'gmail', usernameVariable: 'SMTP_USERNAME', passwordVariable: 'SMTP_PASSWORD')])
                        {emailext (
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
                        )}
                    }
                }
            }
        }

        stage('Create Data Directory') {
            steps {
                // Membuat folder dataCsvTemp jika belum ada
                sh 'mkdir -p /var/lib/jenkins/dataCsvTemp'

                // Menghapus folder dataCsvTemp jika sudah ada
                sh 'rm -rf /var/lib/jenkins/dataCsvTemp/finance-dept_transaksi-penjualan-retail_pg-to-ora.csv'
            }
    
            post {
                failure {
                    script{ 
                        // Send HTML-formatted email notification only when the build fails
                        withCredentials([usernamePassword(credentialsId: 'gmail', usernameVariable: 'SMTP_USERNAME', passwordVariable: 'SMTP_PASSWORD')])
                        {emailext (
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
                        )}
                    }
                }
            }
        }
        stage('Get Data Postgre') {
            steps {
                script {
                    // Read SQL script from file
                    def sqlScript = readFile('selectPG.sql')
                    // Run SQL script to import data from PostgreSQL to CSV
                    sh "PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -p ${PG_PORT} -d ${PG_DATABASE} -U ${PG_USER} -c \"${sqlScript}\""
                }
            }
    
            post {
                failure {
                    script{ 
                        // Send HTML-formatted email notification only when the build fails
                        withCredentials([usernamePassword(credentialsId: 'gmail', usernameVariable: 'SMTP_USERNAME', passwordVariable: 'SMTP_PASSWORD')])
                        {emailext (
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
                        )}
                    }
                }
            }
        }

        stage('Insert Data Oracle') {
            steps {
                script {
                    // Read SQL script from file
                    def insertScript = readFile('insertOra.sql')
                    
                    // Run SQL script to insert data from CSV into Oracle
                    sh "sqlplus -S ${ORACLE_USER}/${ORACLE_PASSWORD}@${ORACLE_SID} @- <<EOF\n${insertScript}\nEOF"
                }
            }
    
            post {
                failure {
                    script{ 
                        // Send HTML-formatted email notification only when the build fails
                        withCredentials([usernamePassword(credentialsId: 'gmail', usernameVariable: 'SMTP_USERNAME', passwordVariable: 'SMTP_PASSWORD')])
                        {emailext (
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
                        )}
                    }
                }
            }
        }
    }
}