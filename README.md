# openshift-test-pipeline
A pipeline for running tests against an OpenShift cluster.

## What is deployed?

* A [persistent Jenkins](setup-pipeline.sh) given a volume capacity of 50Gi.

* A [pipeline](jenkins-pipelines/openshift-test-slave.yaml) to [build, test and push](jenkins-pipelines/Jenkinsfile) a [custom Jenkins slave](docker/dockerfile) based off of the image **jenkins-slave-base-rhel7:latest**.

* An [OpenShift secret](jenkins-pipelines/secret.yaml), used to pass to the Jenkins test pipeline via a generic webhook.

* An [OpenShift test pipeline](jenkins-pipelines/test-pipeline.yaml) which uses a [Jenkinsfile](Jenkinsfile) to run tests against an OpenShift cluster.

## Prerequisites

* Ensure the host you are running `setup-pipeline.sh` and `run-pipeline.sh` are logged in to a OpenShift cluster with appropriate permissions.

## Usage

1. Run the setup script using the following command: `chmod +x setup-pipeline.sh && setup-pipeline.sh`

2. Wait for the **openshift-test-pipeline-slave-pipeline** to finish building the slave image.

3. Provide the required secrets in `jenkins-pipelines/secret.yaml`:

    * Create the secret in the project using the following command: `oc create -f jenkins-pipelines/secret.yaml`

4. Run the test pipeline using the following command: `chmod +x run-pipeline.sh && run-pipeline.sh`