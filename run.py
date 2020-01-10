try:
    from requests import post
    from base64 import b64decode
    from yaml import safe_load, safe_dump
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
    pass


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
    if not all(webhook_url, secret):
        raise ValueError("Required parameters webhook_url and secret were not defined.")
    # Load credentials file in yaml format.
    credentials = load_credentials(credentials_path)
    for num, env_var in enumerate(credentials["env"]):
        name = env_var["name"]
        value = env_var["value"]
        if name != "Sshkey":
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
        print(resp.json())


if __name__ == "__main__":
    fire.Fire({"run_pipeline": run_pipeline, "setup_pipeline": setup_pipeline})

