# Getting Started
Pignus is currently built to run on AWS. Pignus utilizes AWS Lambda, CodeBuild, ECR and RDS to
perform. Full installation docs can be found at [Pignus Getting Started](docs/getting-started.md).

To use Pignus you'll need to run the Pignus Api service in your AWS account. Pignus uses Aws ApiGateway, Lambda, RDS and CodeBuild to perform it's opperations. All of which are deployed and managed by the Terraform project in the `terraform/pignus-api/` directory.

## Adding Pignus to a New AWS Account
We'll use the variable `{account}` as a slug name for the AWS account we're adding Pignus to.
1. Create an Aws ApiGateway api key for Sentry Auth `Sentry-Auth-{account}-Acct`.
2. Create a bucket for secops terraform state files.
3. Create Terraform variable files
 - Create `pignus/terraform/sentry-auth-secrets/{acct}-backend-config.tfvars` enter the secops tf bucket
 - Create `pignus/terraform/sentry-auth/{acct}-backend-config.tfvars`
 - Create `pignus/terraform/sentry-auth/{acct}.tfvars`
4. Run the Sentry Auth Secrets terraform, 
  - Run the command at `pignus/terraform/sentry-auth-secrets`
    ```console
    ACCT=new
    terraform init -reconfigure -backend-config vars/${ACCT}-backend-config.tfvars
    terraform apply
    ```
  - Add the  `Sentry-Auth-{account}-Acct` key when prompted.
5. Run the Sentry Auth terraform
  - Run the command at `pignus/terraform/sentry-auth`
    ```console
    ACCT=new
    terraform init -reconfigure -backend-config vars/${ACCT}-backend-config.tfvars
    terraform apply -var-file vars/${ACCT}.tfvars
    ```
6. Get a copy of the Pignus Docker container into the ECR account.
   This is a little clunky now but will get better over time.

## Adding Pignus to a Kubernetes Cluster
To add Pignus monitoring to a cluster there are a series of steps to follow. If adding monitoring to
a cluster within an AWS account where Pignus is already working there are significantly less steps.
Both scenarios are described below.
We'll use the variable `{cluster}` as a slug name for the Kubernetes cluster we're adding Pignus to.
1. Create an Aws ApiGateway api key for Sentry Auth `Cluster-{cluster}`.
2. Create the `secops` namespace if it doesn't exist.
3. Add the Cluster-{cluster} secret to the Kubernetes cluster
  ```console
  kubectl create namespace secops
  ```
  - Encode the secret as base64
    ```console
    echo -n "the-key" | base64
    ```
  - Create the following yaml with the encoded key
    ```yaml
    apiVersion: v1
    data:
      key: yourbase64==
    kind: Secret
    metadata:
      name: pignus
      namespace: secops
    type: Opaque
    ```
  - Apply the secret `kubectl -n secops apply -f secret.yaml`
4. Run the helm install/upgrade command
    values.
    ```console
    helm upgrade \
      --install \
      pignus-theia \
      ./helm/theia  \
      -n secops \
      -f ./helm/theia/values.yaml \
      -f ./helm/theia/${cluster}-values.yaml
    ```

## Using the Pignus CLI
 - Download and install the Pignus python client tool
   ```console
   git clone git@github.com:PatchSimple/pignus.git
   cd pignus/src/
   pip3 install -r requirements.txt
   python3 setup.py build
   python3 setup.py install
   ```
 - Request an API key and set it
   ```console
   export PIGNUS_API_KEY="your-given-key"
   export PIGNUS_API_URL=""
