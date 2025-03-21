# AWS Lambda with AWS CLI

Create and deploy a lambda function using AWS CLI.

## Create

```shell
# Create a role (once).  Save the ARN.
$ ./scripts/create-role.sh #Outputs ARN...

# Build a deployment package and deploy as a new lambda function
$ ./scripts/build.sh
$ ./scripts/create-function.sh <arn>
```

## Read

```shell
$ ./scripts/list-functions.sh
$ ./scripts/list-roles.sh
```


## Run

```shell
$ ./scripts/run-function.sh
```


## Destroy

```shell
$ ./scripts/delete-function.sh
$ ./scripts/delete-role.sh
```
