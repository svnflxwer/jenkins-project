pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Monitor CRON Jobs') {
            steps {
                script {
                    def scriptPath = "${WORKSPACE}\\monitor_cron_jobs.py"
                    def scriptOutput = sh(script: "python ${scriptPath}", returnStdout: true).trim()
                    echo "Python Script Output:\n${scriptOutput}"

                    // Extract the JSON portion from the script output
                    def startIndex = scriptOutput.indexOf('[')
                    def endIndex = scriptOutput.lastIndexOf(']')
                    def jsonOutput = scriptOutput.substring(startIndex, endIndex + 1)

                    // Parse the JSON output from the Python script
                    def jsonData = readJSON text: jsonOutput
                    def offlineJobs = jsonData as List<String>

                    // Iterate over offline jobs
                    for (def jobName : offlineJobs) {
                        echo "Offline Job: ${jobName}"
                    }
                    currentBuild.description = jsonData as String
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
                                subject: 'CRON Jobs Status',
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