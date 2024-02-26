pipeline {
    agent any

    environment {
        LD_LIBRARY_PATH = '/var/lib/jenkins/instantclient_11_2'
        ORACLE_HOME     = '/var/lib/jenkins/instantclient_11_2'
        CSV_FILE_PATH   = '/var/lib/jenkins/dataCsvTemp'
        SQL_FILE_PATH   = '/var/lib/jenkins/workspace/finance-dept_transaksi-penjualan-retail_ora-to-pg'
        PG_HOST         = 'localhost'
        PG_PORT         = '5432'
        PG_DATABASE     = 'dummydb'
        PG_USER         = 'postgres'
        PG_PASSWORD     = 'sinatriaba'
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
                            to: "sinatria.b.adil@sat.co.id",
                            replyTo: "sinatria.b.adil@sat.co.id",
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
                sh 'rm -rf ${CSV_FILE_PATH}/finance-dept_transaksi-penjualan-retail_ora-to-pg.csv'
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
                            to: "sinatria.b.adil@sat.co.id",
                            replyTo: "sinatria.b.adil@sat.co.id",
                            mimeType: 'text/html'
                        )}
                    }
                }
            }
        }

        stage('Get Data Oracle') {
            steps {
                script {
                    sh 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}'
                    sh 'export ORACLE_HOME=${ORACLE_HOME}'
                    sh 'export PATH=${ORACLE_HOME}:${PATH}'
                    sh 'export TNS_ADMIN=${ORACLE_HOME}/network/ADMIN'

                    // Menjalankan SQL script untuk export data dari Oracle ke CSV
                    sh 'sqlplus jenkinsdb/sinatriaba@XE @/var/lib/jenkins/workspace/finance-dept_transaksi-penjualan-retail_ora-to-pg/selectOra.sql'
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
                            to: "sinatria.b.adil@sat.co.id",
                            replyTo: "sinatria.b.adil@sat.co.id",
                            mimeType: 'text/html'
                        )}
                    }
                }
            }
        }

        stage('Get Data Postgre') {
            steps {
                script {
                    // Menjalankan SQL script untuk  import data dari CSV ke PostgreSQL
                    sh "psql -h ${PG_HOST} -p ${PG_PORT} -d ${PG_DATABASE} -U ${PG_USER} -c \"COPY transaksi_penjualan_retail(id_transaksi, id_franchaise, franchaise, tanggal_transaksi, id_produk, nama_produk, jumlah_terjual, stock, discount, PPN, PPH4, PPH23, status_pembayaran, tanggal_pembayaran) FROM '${CSV_FILE_PATH}/insertPG.sql' DELIMITER '|' CSV HEADER;\""
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
                            to: "sinatria.b.adil@sat.co.id",
                            replyTo: "sinatria.b.adil@sat.co.id",
                            mimeType: 'text/html'
                        )}
                    }
                }
            }
        }
    }
}
