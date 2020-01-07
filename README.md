# openshift-test-pipeline
A pipeline for running tests against an OpenShift cluster.

## Prerequisites

* Ensure the host you are running `setup-pipeline.sh` is logged in to a OpenShift cluster with appropriate permissions.

## Usage

1. Run the setup script:

    * `chmod +x setup-pipeline.sh`

    * Execute `./setup-pipeline.sh`

2. Once the `openshift-test-pipeline-slave-pipeline` has completed all builds, run the pipeline:

    * `chmod +x setup-pipeline.sh`

    * Execute `./run-pipeline.sh`