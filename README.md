# openshift-test-pipeline
A pipeline for running tests against an OpenShift cluster.

## Prerequisites

* Ensure the host you are running `setup-pipeline.sh` and `run-pipeline.sh` are logged in to a OpenShift cluster with appropriate permissions.

## Usage

1. Run the setup script using the following command: `chmod +x setup-pipeline.sh && setup-pipeline.sh`

2. Wait for the **openshift-test-pipeline-slave-pipeline** to finish building the slave image.

3. Provide the required secrets in `jenkins-pipelines/secret.yaml`:

    * Create the secret in the project using the following command: `oc create -f jenkins-pipelines/secret.yaml`

4. Run the test pipeline using the following command: `chmod +x run-pipeline.sh && run-pipeline.sh`