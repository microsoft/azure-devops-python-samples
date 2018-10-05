# Python samples for Azure DevOps

This repository contains Python samples that show how to integrate with Azure DevOps and Team Foundation Server (TFS) using the [Azure DevOps Python API](https://github/Microsoft/vsts-python-api/).

## Explore

Samples are organized by "area" (service) and "resource" within the `samples` package.
Each sample module shows various ways for interacting with Azure DevOps and TFS.
Resources may have multiple samples, since there are often multiple ways to query for a given resource.

## Installation

1. Clone this repository and `cd` into it

2. Create a virtual environment (`python3 -m venv env && . env/bin/activate && pip install -r requirements.txt`)

Now you can run `runner.py` with no arguments to see available options.

## Run the samples - command line

> **VERY IMPORTANT**: some samples are destructive! It is recommended that you run these samples against a test organization.

1. Get a [personal access token](https://docs.microsoft.com/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=vsts).

2. Store the PAT and organization URL you'll be running samples against (note: some samples are destructive, so use a test organization):
   * `runner.py config url --set-to https://fabrikam.visualstudio.com`
   * `runner.py config pat --set-to ABC123`
   * If you don't want your PAT persisted to a file, you can put it in an environment variable called `VSTS_PAT` instead

3. Run `runner.py run {area} {resource}` with the 2 required arguments:
   * `{area}`: API area (currently core, git, and work_item_tracking) to run the client samples for. Use `all` to include all areas.
   * `{resource}`: API resource to run the client samples for. Use `all` to include all resources.
   * You can optionally pass `--url {url}` to override your configured URL

### Examples

#### Run all samples

```
python runner.py run all all
```

#### Run all work item tracking samples

```
python runner.py run work_item_tracking all
```

#### Run all Git pull request samples

```
python runner.py run git pullrequests
```

#### Run all Git samples against a different URL than the one configured; in this case, a TFS on-premises collection

```
python runner.py run git all --url https://mytfs:8080/tfs/testcollection
```

### Save request and response data to a JSON file

To persist the HTTP request/response as JSON for each client sample method that is run, set the `--output-path {value}` argument. For example:

```
python runner.py run all all --output-path ~/temp/http-output
```

This creates a folder for each area, a folder for each resource under the area folder, and a file for each client sample method that was run. The name of the JSON file is determined by the name of the client sample method. For example:

```
|-- temp
    |-- http-output
        |-- git
            |-- refs
                |-- get_refs.json
                |-- ...
            |-- repositories
                |-- get_repositories.json
                |-- ...
```

Note: certain HTTP headers like `Authorization` are removed for security/privacy purposes.

## See what samples are available

You can run `runner.py list` to see what sample areas and resources are available.

## Run the samples - Jupyter notebook

We also provide a Jupyter notebook for running the samples.
You'll get a web browser where you can enter URL, authentication token, and choose which samples you wish to run.

1. Clone this repository and `cd` into it

2. Create a virtual environment (`python3 -m venv env && . env/bin/activate && pip install -r requirements.jupyter.txt`)

3. Get a personal access token.

4. Run `jupyter notebook`. In the resulting web browser, click **API Samples.ipynb**.

5. Click **Run** in the top cell. Scroll down and you'll see a form where you can enter your organization or TFS collection URL, PAT, and choose which samples to run.

> **IMPORTANT**: some samples are destructive. It is recommended that you first run the samples against a test account.

## Contribute

This project welcomes contributions and suggestions.
Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution.
For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment).
Simply follow the instructions provided by the bot.
You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

See detailed instructions on how to [contribute a sample](./contribute.md).
