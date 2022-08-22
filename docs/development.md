# Pignus Development
To develop on Pignus, download the repository and set an environment variable, `PIGNUS_PATH` to the
location where Pignus is installed. Details on developing each piece of Pignus are described below.

## General Development
Set the following ENV vars with applicablible values to your environment.
```console
PIGNUS_PATH="/User/name/pignus"
```

## Terraform
Pignus has 5 different Terraform projects, described below in order of necessity. All of these
projects should be setup using the following pattern within the terraform projects dir. To setup
the Terraform, set the ACCT var equal to the name of the config var/ account you will be
developing under.
```console
ACCT=my_account_name
terraform init -reconfigure -backend-config vars/${ACCT}-backend-config.tfvars
```
### Pignus-Api-Secrets
Located at `pignus/terraform/pignus-api-secrets`. This Terraform project builds the necessary
the secrets Pignus Api will need.
 - A KMS key, used to encrypt ECR repositories, RDS data and Pignus secrets in AWS SSM.
 - SSM Paramater `PIGNUS_RDS_ADMIN_USER`: The RDS admin user name.
 - SSM Paramater `PIGNUS_RDS_ADMIN_PASS`: The RDS admin user password.
 - SSM Paramater `PIGNUS_RDS_APP_USER`: The RDS Pignus application user name.
 - SSM Paramater `PIGNUS_RDS_APP_PASS`: The RDS Pignus application user password.
 - SSM Paramater `PIGNUS_API_KEY`: This is depricated and will be removed shortly.

### Pignus-Api
Located at `pignus/terraform/pignus-api`. This Terraform project builds all the components of the Pignus Api. 

### Pignus-CICD
Located at `pignus/terraform/pignus-cicd`. This Terraform project builds all the components of the Pignus CICD process.

### Pignus-Auth
Located at `pignus/terraform/pignus-auth`.

### Pignus-Auth-Secrets
Located at `pignus/terraform/pignus-auth-secrets`.

## Pignus CLI/ API, Sentry and Theia
The Pignus CLI, API, Sentry and Theia are all developed under the Python code in `pignus/src/`
directory. They can be installed by,
```console
cd pignus/src/
python3 setup.py build
python3 setup.py install
```

## Sentry Auth
Sentry Auth gives an AWS account permissions to pull ECR images from one account to another. This is
done by deploying a lambda that lives in the AWS accounts where the ECR repositories live ie Dev and
 Prod accounts for now.

## Theia
The Theia cluster monitor is deployed to a Kubernetes and monitors images being deployed to the
cluster.

### Debugging Theia
To run the Kubernetes cronjob manually once the cronjob has been deployed to the cluster, use the
following command.
```console
kubectl create job -n secops --from=cronjob/pignus-theia pignus-theia-manual-001
```

## Testing
### Unit Tests
Unit tests are managed by pytest, and can be found in [tests/unit](../tests/unit).
To execute unit tests go to the unit test dir and run `pytest -vvv`.
To get test coverage `pytest -vv --cov=pignus --cov-report term-missing`
Current unit test coverage at _49%_ with 261 unit tests.
### Regression Tests
Regression tests are managed by pytest, and can be found in [tests/regression](../tests/regression).
They cover each of the entities the API currently exposes.

## Releasing a New Version
When pressing a new sem ver the following files will need to be updated.
`README.md`
`/pignus/src/pignus/version.py`


# Helper Commands
Random smattering of helper commands used in developing/ working with Pignus.

kubectl create job -n secops --from=cronjob/pignus-theia pignus-theia-manual-001

helm upgrade \
  --install \
  pignus-theia \
  ./helm/theia  \
  -n secops \
  -f ./helm/theia/values.yaml \
  -f ./helm/theia/stage-values.yaml
```
