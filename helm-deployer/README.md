# Helm Deployment and Dependency Management with Git Submodules

This repo deploys Helm charts, stored as git submodules, to the attached Kubernetes cluster.

## Cloning this Repository

To clone this repository use:

`$ git clone https://gitlab.ep.shell.com/dev/ep/de/helm-deployer.git --recurse-submodules`

or, if you have already cloned the repo without the submodules, you can run:

`$ git submodule init` 

followed by:

`$ git submodule update`

## Repository Structure

`/`: In the root directory you will find this readme, the `gitlab-ci.yml` file, and the `.gitmodules` file. The `.gitmodules` contains a list of git submodules that point to the Helm charts required for the team. It is created and updated using the `git submodule` command, and should not be edited manually.

`/charts`: This folder contains any Helm charts that need to be deployed. Any additional charts should be added using `git submodule add ${REPO_URL} charts/${APP_NAME}`, and can be updated with `git submodule update`.

`/values`: This folder contains the Helm values files for the deployments.

`/scripts`: Here you will find any scripts required by the pipeline. For now there is a script to generate the downstream pipelines, and one to test that there is a values file present for each Helm chart.

## Adding a new chart

To add a new Helm chart to the repository add it as a git submodule, using a relative path if the repository is hosted on the same gitlab server:

`$ git submodule add ../<ORG>/<REPO> charts/<DEPLOYMENT_NAME>`

or an absolute path if it is hosted elsewhere:

`$ git submodule add https://<GIT_SERVER>/<ORG>/<REPO> charts/<DEPLOYMENT_NAME>`

## Adding a custom values file

To add a values file to configure your chart, copy the values file from the `/charts/<DEPLOYMENT_NAME>/chart/` directory to `/values/<DEPLOYMENT_NAME>.yaml` and make any changes needed for the environment. If the values file is not present or named incorrectly, the test stage will fail.

## Secret Management

To pass a secret to your helm deployment, it should be added to [Settings -> CI/CD -> Variables](https://gitlab.ep.shell.com/dev/ep/de/helm-deployer/-/settings/ci_cd). The variable name (key) should be the secret name, prefixed with `K8S_SECRET_` and should be scoped to the application environment(s) as necessary.

Note: Hyphens are not supported in environment variables, so should not be used in secret names.

## Disabling an application deployment

To disable an application deployment, add a variable to [Settings -> CI/CD -> Variables](https://gitlab.ep.shell.com/dev/ep/de/helm-deployer/-/settings/ci_cd) with the key `DISABLE_<DEPLOYMENT_NAME>` and a value of `true` (i.e. DISABLE_AIRFLOW=true).