# openshift-test-pipeline

A pipeline for running tests against an OpenShift cluster.

## What is deployed?

* A persistent Jenkins instance with a volume capacity of 50Gi.

* A [pipeline](jenkins-pipelines/openshift-test-slave.yaml) to [build, test and push](jenkins-pipelines/Jenkinsfile) a [custom Jenkins slave](docker/dockerfile) based off of the image **jenkins-slave-base-rhel7:latest**.

* An [OpenShift test pipeline](jenkins-pipelines/test-pipeline.yaml) which uses a [Jenkinsfile](Jenkinsfile) to run tests against an OpenShift cluster.

## Prerequisites

* The [OKD/OC CLI](https://www.okd.io/download.html) and be logged into an OpenShift cluster with appropriate permissions

* Python 3.7

* Install the requirements for the Python CLI using the following command: `pip install -r requirements.txt`

## Usage

1. Fill out the [`credentials.yaml`](credentials.yaml) file with the required fields **in base64 format** for the test-pipeline.

    * This file is used to pass environment variables to Jenkins in order to run tests on the OpenShift cluster.

2. Use [run.py](run.py) to setup the pipeline using the following command:

    ```bash
    # Use setup_pipeline first.
    # You can also supply no parameters to use all the defaults.
    # To specify specific parameters. Prefix with --<parametername>=<parametervalue>
    python run.py setup_pipeline [name] [source_repository_url] [source_repository_ref] [context_dir] [pipeline_context_dir] [project]
    ```

3. Use [run.py](run.py) to run the pipeline using the following command:

    ```bash
    python run.py run_pipeline [credentials_path] [webhook_url] [secret]
    # Example:
    python run.py run_pipeline credentials.yaml https://ocp.somedomain.com:8443/apis/build.openshift.io/v1/namespaces/test-pipeline/buildconfigs/openshift-test-pipeline/webhooks/<secret>/generic b1c65552-c8e2-4620-b2fd-8ba84f3e8dd2
    ```
