node ("openshift-test-pipeline-slave") {

    try {

        stage("Create SSH key") {
            sh("printenv")
            sh("""
                echo \$Sshkey | tee -a ssh_key
                chmod 600 ssh_key
            """)
        }

        stage ("Validate OpenShift deployment") {
            sh("""
                ssh -o StrictHostKeyChecking=no -i ssh_key cloud-user@${env.BASTION_IP} "ansible-playbook -i /usr/share/ansible/openshift-deployment-ansible/openshift-ansible-hosts /usr/share/ansible/openshift-deployment-ansible/tests/all.yml \
                    --extra-vars OPENSHIFT_USERNAME=${env.OPENSHIFT_USERNAME} \
                    --extra-vars OPENSHIFT_PASSWORD=${env.OPENSHIFT_PASSWORD} \
                    --extra-vars ADMIN_USERNAME=${env.ADMIN_USERNAME} \
                    --extra-vars ADMIN_PASSWORD=${env.ADMIN_PASSWORD} \
                    --extra-vars domainSuffix=${env.DOMAIN_SUFFIX}
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
