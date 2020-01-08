# openshift-test-pipeline
A pipeline for running tests against an OpenShift cluster.

## Prerequisites

* Ensure the host you are running `setup-pipeline.sh` and `run-pipeline.sh` are logged in to a OpenShift cluster with appropriate permissions.

## Usage

1. Run the setup script:

    * `chmod +x setup-pipeline.sh`

    * Execute `setup-pipeline.sh`

2. Once the `openshift-test-pipeline-slave-pipeline` has completed all builds, run the test pipeline:

    **NOTE:**

    * If running manually, ensure you have an OpenShift secret named **openshift**

        * If not, base64 encode all your secrets and provide them in `jenkins-pipelines/secret.yaml`

        * To create the secret, execute the command: `oc create -f jenkins-pipelines/secret.yaml`

    * `chmod +x setup-pipeline.sh`

    * Execute the command: `run-pipeline.sh`