try:
    from requests import post
    from base64 import b64decode
    from yaml import safe_load, safe_dump
    from subprocess import call
    from uuid import uuid4
    import fire

    # Imports for error handling.
    from yaml.parser import ParserError
    import binascii
except ImportError as err:
    raise ImportError(f"Failed to import required modules: {err}")


def setup_pipeline(
    name: str = "openshift-test-pipeline-slave",
    source_repository_url: str = "https://github.com/UKCloud/openshift-test-pipeline.git",
    source_repository_ref: str = "dev",
    context_dir: str = "docker",
    pipeline_context_dir: str = "jenkins-pipelines",
    project: str = "test-pipeline",
):
    """
    Setup the test pipeline.
    :param name: The name of the jenkins slave creation pipeline.
    :param source_repository_url: The url to this Github repository, to pull required resources.
    :param source_repository_ref: The specific ref/branch to pull.
    :param context_dir: The context directory where the dockerfile for the jenkins slave resides.
    :param pipeline_context_dir: The directory containing pipeline files.
    :param project: The project name to create in OpenShift.
    """
    # Create OpenShift project.
    call(["oc", "new-project", project])
    # Create persistent Jenkins in OpenShift with Slack plugins.
    call(
        [
            "oc",
            "new-app",
            "jenkins-persistent",
            "-p",
            "VOLUME_CAPACITY=50Gi",
            "-e",
            "INSTALL_PLUGINS=slack:2.35,global-slack-notifier:1.5",
        ]
    )
    # Deploy Jenkins slave pipeline.
    # Using Subprocess for the following commands as OpenShift Python rest client doesn't support templating.
    call(
        [
            "oc",
            "new-app",
            "-f",
            "jenkins-pipelines/openshift-test-slave.yaml",
            "-p",
            f"NAME={name}",
            "-p",
            f"SOURCE_REPOSITORY_URL={source_repository_url}",
            "-p",
            f"SOURCE_REPOSITORY_REF={source_repository_ref}",
            "-p",
            f"CONTEXT_DIR={context_dir}",
            "-p",
            f"PIPELINE_CONTEXT_DIR={pipeline_context_dir}",
        ]
    )
    # Generate random UUID for generic webhook secret.
    secret = uuid4()
    # Deploy buildconfig for test pipeline. Creates generic webhook.
    call(
        [
            "oc",
            "new-app",
            "-f",
            "jenkins-pipelines/test-pipeline.yaml",
            "-p",
            f"SECRET={secret}",
            "-p",
            f"SOURCE_REPOSITORY_REF={source_repository_ref}",
        ]
    )
    # Once created, describe object telling the user how to kick off a pipeline.
    call(["oc", "describe", "bc/openshift-test-pipeline"])
    print(
        "Use the generic webhook URL to begin the test-pipeline. This will require you to make a HTTP POST request manually.\nIt is recommended to use the run_pipeline command."
    )


def load_credentials(credentials_path: str):
    """
    Helper function to load required credentials from a file on the host.
    :rtype credentials: dict()
    """
    # Load credentials file.
    try:
        with open(credentials_path) as cred_file:
            credentials = safe_load(cred_file.read())
        return credentials
    except IOError:
        raise IOError(f"Failed to open file: {credentials_path}")
    except ParserError as err:
        raise ParserError(
            f"Failed to convert file: {credentials_path} to Python dictionary: {err}"
        )


def run_pipeline(
    credentials_path: str = "credentials.yaml",
    webhook_url: str = None,
    secret: str = None,
):
    """
    Runs the test pipeline.
    :param credentials_path: The path to the credentials file on the host.
    :param webhook_url: The webhook url to trigger the test pipeline.
    :param secret: The secret to provide in the webhook url.
    """
    # Check that both webhook_url and secret are not None.
    REQUIRED_PARAMS = (webhook_url, secret)
    if not all(REQUIRED_PARAMS):
        raise ValueError("Required parameters webhook_url and secret were not defined.")
    # Load credentials file in yaml format.
    credentials = load_credentials(credentials_path)
    for num, env_var in enumerate(credentials["env"]):
        name = env_var["name"]
        value = env_var["value"]
        # Base64 decode all values apart from SSHKEY.
        # Sshkey isn't decoded to preserve formatting.
        if name != "SSHKEY":
            try:
                # Decode base64 encoded string.
                decoded_string = b64decode(value).decode("utf-8")
                # Update dictionary at runtime with decoded string.
                credentials["env"][num]["value"] = decoded_string
            except binascii.Error:
                raise ValueError(
                    f"The value: {value} for environment variable: {name} is not base64 encoded."
                )
    # Prepare yaml payload for webhook request.
    credentials_yaml = safe_dump(credentials, default_flow_style=False)
    # Replace "<secret>" in webhook_url with secret provided.
    webhook_url = webhook_url.replace("<secret>", secret)
    # Make webhook request.
    resp = post(
        url=webhook_url,
        headers={"Content-Type": "application/yaml"},
        data=credentials_yaml,
    )
    if resp.status_code != 200:
        # Raise HTTPError.
        resp.raise_for_status()
    else:
        print(resp.content)


if __name__ == "__main__":
    __version__ = "0.0.1"
    fire.Fire({"run_pipeline": run_pipeline, "setup_pipeline": setup_pipeline})

