node ("openshift-test-pipeline-slave") {

    try {

        stage("Create SSH key") {
            sh("""
                echo \$SSHKEY | base64 -d | tee -a ssh_key
                chmod 600 ssh_key
            """)
        }

        stage ("Validate OpenShift deployment") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tests/all.yml \
                    --extra-vars OPENSHIFT_USERNAME=\"\$USERNAME\" \
                    --extra-vars OPENSHIFT_PASSWORD=\"\$USERPASS\" \
                    --extra-vars ADMIN_USERNAME=\"\$ADMINUSER\" \
                    --extra-vars ADMIN_PASSWORD=\"\$ADMINPASS\" \
                    --extra-vars domainSuffix=\"\$DOMAINSUFFIX\""
            """)
            }

        /*
            Load tests for cluster using Locust.
        */
        stage('OpenShift load testing') {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP \
                    "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /home/cloud-user/openshift-tooling/locust/locust_setup.yaml --extra-vars domainSuffix=\"\$DOMAINSUFFIX\""
            """)
        }

        stage("Validate cluster cronjobs") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/backup.yml";
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP "ansible-playbook -v -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tools/playbooks/docker-prune.yaml";
                
                if [ \"\$MULTINETWORK\" = true ]; then ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tools/playbooks/squid-whitelist.yaml"; fi
            """)
        }

        /*
        Test user creation works (using a randomly-generated password)
        */
        stage("Validate OpenShift user creation") {
            sh("""
                RANDOM_PASSWORD=\$(openssl rand -base64 20 | cut -d= -f1);
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP "cd /usr/share/ansible/openshift-deployment-ansible/tools/ ; ./create-user.sh testUser \$RANDOM_PASSWORD"
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@\$BASTIONIP "oc login https://ocp.\$DOMAINSUFFIX:8443 --insecure-skip-tls-verify=true -u testUser -p \$RANDOM_PASSWORD"
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
