node ("openshift-test-pipeline-slave") {

    try {

        stage("Create SSH key") {
            sh("""
                echo \$Sshkey | base64 -d | tee -a ssh_key
                chmod 600 ssh_key
            """)
        }

        stage ("Validate OpenShift deployment") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tests/all.yml \
                    --extra-vars OPENSHIFT_USERNAME=\"\$Username\" \
                    --extra-vars OPENSHIFT_PASSWORD=\"\$Userpass\" \
                    --extra-vars ADMIN_USERNAME=\"\$Adminuser\" \
                    --extra-vars ADMIN_PASSWORD=\"\$Adminpass\" \
                    --extra-vars domainSuffix=\"\$Domainsuffix\""
            """)
            }

        /*
            Load tests for cluster using Locust.
        */
        stage('openshift load testing') {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip \
                    "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /home/cloud-user/openshift-tooling/locust/locust_setup.yaml --extra-vars domainSuffix=\"\$Domainsuffix\""
            """)
        }

        stage("Validate cluster cronjobs") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/backup.yml";
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip "ansible-playbook -v -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tools/playbooks/docker-prune.yaml";
                
                if [ \"\$MULTINETWORK\" = true ]; then ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tools/playbooks/squid-whitelist.yaml"; fi
            """)
        }

        /*
        Test user creation works (using a randomly-generated password)
        */
        stage("Validate OpenShift user creation") {
            sh("""
                RANDOM_PASSWORD=\$(openssl rand -base64 20 | cut -d= -f1);
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip \
                    "cd /usr/share/ansible/openshift-deployment-ansible/tools/ ; ./create-user.sh testUser \$RANDOM_PASSWORD"
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$Bastionip \
                    "oc login https://ocp.\$Domainsuffix:8443 --insecure-skip-tls-verify=true -u testUser -p \$RANDOM_PASSWORD"
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
