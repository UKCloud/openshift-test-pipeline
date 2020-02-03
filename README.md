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

### Slack Notifications

1. Login to Jenkins via the route exposed by OpenShift

2. On the left menu, click **Manage Jenkins**

3. Scroll down and click **Configure System**

4. Scroll down to the heading **Slack**

5. Set the **workspace** field to the desired Slack workspace

6. Click **Add** next to the **credential** field

7. Click **Jenkins**

8. Click the **Kind** dropdown menu, and click **Secret text**

9. Supply the Slack token in the **secret** field

10. Provide the ID `slack-token`

11. Click **Add**

12. Select the `slack-token` from the **Credential** dropdown menu

13. Set the **Default channel / member id** to the channel you wish to send notifications to

14. To see if notifications are working, click **Test Connection**

15. Once you have verified everything is working, click **Save**
