#!/bin/bash

# Declare variables.
NAME="openshift-test-pipeline-slave"
SOURCE_REPOSITORY_URL="https://github.com/UKCloud/openshift-test-pipeline.git"
SOURCE_REPOSITORY_REF="dev"
CONTEXT_DIR="docker"
PROJECT="test-pipeline"

# Setup pipeline project in OpenShift.
oc new-project $PROJECT

# Switch OpenShift project.
oc project $PROJECT

# Deploy jenkins master.
oc new-app jenkins-persistent -p VOLUME_CAPACITY=50Gi

# Deploy jenkins slave.
oc new-app -f jenkins-pipelines/openshift-test-slave.yaml \
    -p NAME=$NAME \
    -p SOURCE_REPOSITORY_URL=$SOURCE_REPOSITORY_URL \
    -p SOURCE_REPOSITORY_REF=$SOURCE_REPOSITORY_REF \
    -p CONTEXT_DIR=$CONTEXT_DIR

# Start openshift-test-pipeline-slave build.
oc start-build openshift-test-pipeline-slave --follow=true

# Create Base64 string to use as pipeline generic webhook secret.
BASE64STRING=$(echo \$RANDOM | base64)
# Deploy buildconfig for test pipeline. Creates generic webhook.
oc new-app -f jenkins-pipelines/test-pipeline.yaml -p SECRET=$BASE64STRING

# Once created, describe object telling the user how to kick off a pipeline.
oc describe bc/openshift-test-pipeline
echo "Use the Webhook Generic URL above to kick off the pipeline."
