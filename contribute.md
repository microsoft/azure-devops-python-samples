# Contribute to the samples

## Organization and style

1. Samples for an API area should live together under the `samples` package. Each module is an area.
   ```
   |-- src
       |-- samples
           |-- git.py
   ```

2. Within a module, create a method for each sample. Samples are not object-oriented.
   * The name of the method should represent what the sample is demonstrating, e.g. `get_{resource}`:
    ```python
    def get_repos(...):
    ```
   * The method must accept a `context` parameter, which will contain information passed in from the sample runner infrastructure:
    ```python
    def get_repos(context):
    ```
   * The method must decorated with `@resource('resource_name')` to be detected:
    ```python
    from samples import resource

    @resource('repositories')
    def get_repos(context):
    ```
   * Results should be logged using the `utils.emit` function:
    ```python
    from samples import resource
    from utils import emit, find_any_project

    @resource('repositories')
    def get_repos(context):
        project = find_any_project(context)

        git_client = context.connection.get_client("vsts.git.git_client.GitClient")

        repos = git_client.get_repositories(project.id)
        for repo in repos:
            emit(repo)

        return repos
    ```


3. Coding and style
   * Samples should show catching exceptions for APIs where exceptions are common
   * Use line breaks and empty lines to help delineate important sections or lines that need to stand out
   * Use the same "dummy" data across all samples so it's easier to correlate similar concepts
   * Be as Pythonic and PEP8-y as you can be without violating the above principles. `flake8` is your friend, and should run without anything triggering. (Non-standard default: 120-character lines are allowed.)

4. All samples **MUST** be runnable on their own without any input

5. All samples **SHOULD** clean up after themselves.
Have a sample method create a resource (to demonstrate creation).
Have a later sample method delete the previously created resource.
In between the creation and deletion, you can show updating the resource (if applicable)
