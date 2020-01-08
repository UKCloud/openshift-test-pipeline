node ("openshift-test-pipeline-slave") {

    try {

        stage ("Checks and creates envrionment variables") {
            // Check 'Credentials' envrionment variable is not ''.
            if (env.Credentials == "") {
                throw new Exception("Credentials environment variable was empty.")
            }
            else {
                // Setup credential envrionment variables.
                environment {
                    OPENSHIFT_USERNAME = sh("""echo ${env.Credentials} | jq ".['data']['username']" | base64 --decode""")
                    OPENSHIFT_PASSWORD = sh("""echo ${env.Credentials} | jq ".['data']['userpass']" | base64 --decode""")
                    ADMIN_USERNAME = sh("""echo ${env.Credentials} | jq ".['data']['adminuser']" | base64 --decode""")
                    ADMIN_PASSWORD = sh("""echo ${env.Credentials} | jq ".['data']['adminpass']" | base64 --decode""")
                    BASTION_IP = sh("""echo ${env.Credentials} | jq ".['data']['bastionip']" | base64 --decode""")
                    DOMAIN_SUFFIX = sh("""echo ${env.Credentials} | jq ".['data']['domainsuffix']" | base64 --decode""")
                    MULTINETWORK = sh("""echo ${env.Credentials} | jq ".['data']['multinetwork']" | base64 --decode""")
                    SSH_KEY = sh("""echo ${env.Credentials} | jq ".['data']['sshkey']" | base64 --decode""")
                }
            }
        }

        stage("Create SSH key") {
            sh("""
                echo ${env.SSH_KEY} | tee -a ssh_key
                chmod 600 ssh_key
            """)
        }

        stage ("Validate OpenShift deployment") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tests/all.yml \
                    --extra-vars OPENSHIFT_USERNAME=${env.OPENSHIFT_USERNAME} \
                    --extra-vars OPENSHIFT_PASSWORD=${env.OPENSHIFT_PASSWORD} \
                    --extra-vars ADMIN_USERNAME=${ADMIN_USERNAME} \
                    --extra-vars ADMIN_PASSWORD=${ADMIN_PASSWORD} \
                    --extra-vars domainSuffix=${DOMAIN_SUFFIX}
            """)
            }

        stage("Validate cluster cronjobs") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/backup.yml";
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} "ansible-playbook -v -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tools/playbooks/docker-prune.yaml";
                
                if [ ${env.MULTINETWORK} = true ]; then ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tools/playbooks/squid-whitelist.yaml"; fi
            """)
        }

        /*
        Test user creation works (using a randomly-generated password)
        */
        stage("Validate OpenShift user creation") {
            sh("""
                RANDOM_PASSWORD=\$(openssl rand -base64 20 | cut -d= -f1);
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} \
                    "cd /usr/share/ansible/openshift-deployment-ansible/tools/ ; ./create-user.sh testUser \$RANDOM_PASSWORD"
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} \
                    "oc login https://ocp.${env.DOMAIN_SUFFIX}:8443 --insecure-skip-tls-verify=true -u testUser -p \$RANDOM_PASSWORD"
            """)
        }
    }
    catch (e) {
        throw e
    }
    finally {
        echo "Pipeline completed."
    }
}
